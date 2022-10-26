from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply('connected')

@has_log
class AeroflexStreamInterface(StreamInterface):

    in_terminator = '\n'
    out_terminator = '\n'
    
    cfrq_response = ':{}:VALUE {};INC {};MODE {}'
    rflv_response = ':{}:UNITS {};TYPE {};VALUE {};INC {};{}'
    mode_response = ':{} {}'
    
    CAR_FREQ_COMM = 'CFRQ'
    RF_LVL_COMM = 'RFLV'
    MODE_COMM = 'MODE'
    RESET_COMM = '*RST'
    ERROR_COMM = 'ERROR'
    
    CFRQ_INC_VALUE = 1.0
    CFRG_MODE_VALUE = 'FIXED'
    RFLV_TYPE_VALUE = 'EMF'
    RFLV_INC_VALUE = 0.1
    RFLV_STATUS_VALUE = 'ON'

    MULT_FACTOR = {
        'k': 1000,
        'M': 1000000,
        'G': 1000000000
    }
    
    def __init__(self):
        super(AeroflexStreamInterface, self).__init__()
        
        self.commands = {
            CmdBuilder(self.get_carrier_freq).escape(self.CAR_FREQ_COMM.lower() + '?').eos().build(),
            CmdBuilder(self.get_rf_level).escape(self.RF_LVL_COMM.lower() + '?').eos().build(),
            CmdBuilder(self.get_modulation).escape(self.MODE_COMM.lower() + '?').eos().build(),
            CmdBuilder(self.reset).escape(self.RESET_COMM).eos().build(),
            CmdBuilder(self.get_error).escape(self.ERROR_COMM.lower() + '?').eos().build(),
            
            CmdBuilder(self.set_carrier_freq).escape(self.CAR_FREQ_COMM + ':VALUE ').any().eos().build(),
            CmdBuilder(self.set_rf_level).escape(self.RF_LVL_COMM + ':VALUE ').float().eos().build(),
            CmdBuilder(self.set_modulation).escape(self.MODE_COMM + ' ').string().eos().build(), 
        }
        
    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error('An error occurred at request ' + repr(request) + ': ' + repr(error))
        
        return ''
    
    def get_carrier_freq(self):
        return self.cfrq_response.format(self.CAR_FREQ_COMM, self._device.carrier_freq_val, self._device.carrier_freq_inc, self._device.carrier_freq_mode)
	
    def get_rf_level(self):
        return self.rflv_response.format(self.RF_LVL_COMM, self._device.rf_lvl_unit, self._device.rf_lvl_type, self._device.rf_lvl_val, self._device.rf_lvl_inc, self._device.rf_lvl_status)
	
    def get_modulation(self):
        return self.mode_response.format(self.MODE_COMM, self._device.modulation_mode)
        
    def reset(self):
        self._device.carrier_freq_val = 0
        self._device.rf_lvl_val = 0
        self._device.modulation_mode = 'AM'
        
        return ''
        
    def get_error(self):
        return self._device.error
        
    def set_carrier_freq(self, new_carrier_freq):
        new_carrier_freq_val = new_carrier_freq.split('H')[0]

        if new_carrier_freq_val[-1:].isnumeric():
            self._device.carrier_freq_val = float(new_carrier_freq_val)
        else: 
            self._device.carrier_freq_val = float(new_carrier_freq_val[:-1]) * self.MULT_FACTOR[new_carrier_freq_val[-1:]]
        
        return ''
	
    def set_rf_level(self, new_rf_lvl_val):
        self._device.rf_lvl_val = new_rf_lvl_val
        
        return ''
	
    def set_modulation(self, new_modulation_mode):
        cleaned_input = new_modulation_mode.replace('1','')
        split_modulation_val = cleaned_input.split('m')[0]
        self._device.modulation_mode = split_modulation_val
        
        return ''

