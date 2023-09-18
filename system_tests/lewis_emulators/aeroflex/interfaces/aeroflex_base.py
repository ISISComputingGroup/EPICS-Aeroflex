from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply('connected')

'''
Stream device for Aeroflex
'''

@has_log
class CommonStreamInterface(object):

    in_terminator = '\n'
    out_terminator = '\n'

    MULT_FACTOR = {
        'k': 1000,
        'M': 1000000,
        'G': 1000000000
    }
    
    commands = [
            CmdBuilder('get_carrier_freq').escape('CFRQ?').eos().build(),
            CmdBuilder('get_rf_level').escape('RFLV?').eos().build(),
            CmdBuilder('get_modulation').escape('MODE?').eos().build(),
            CmdBuilder('get_modulation_control').escape('MOD?').eos().build(),
            CmdBuilder('reset').escape('*RST').eos().build(),
            CmdBuilder('get_error').escape('ERROR?').eos().build(),
            
            CmdBuilder('set_carrier_freq').escape('CFRQ:VALUE ').any().eos().build(),
            CmdBuilder('set_rf_level').escape('RFLV:VALUE ').float().eos().build(),
            CmdBuilder('set_modulation').escape('MODE ').string().eos().build(), 
            CmdBuilder('set_modulation_control').escape('MOD ').string().eos().build(), 

            CmdBuilder('set_rf_on').escape('RFLV:ON').eos().build(),
            CmdBuilder('set_rf_off').escape('RFLV:OFF').eos().build(),
            CmdBuilder('get_pulse_modulation').escape('PULSE?').eos().build(),
            CmdBuilder('get_pulse_cw').escape('PULSE:CAL?').eos().build(),
            CmdBuilder('get_fm_modulation').escape('FM').int().escape('?').eos().build(),
            CmdBuilder('get_am_modulation').escape('AM').int().escape('?').eos().build(),
            CmdBuilder('get_pm_modulation').escape('PM').int().escape('?').eos().build(),
            CmdBuilder('get_wbfm_modulation').escape('WBFM?').eos().build(),
            
    ]
        
    def handle_error(self, request, error):
        '''
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        '''
        self.log.error('An error occurred at request ' + repr(request) + ': ' + repr(error))
        
        return ''
    
    def get_rf_level(self):
        return f':RFLV:UNITS {self._device.rf_lvl_unit};TYPE {self._device.rf_lvl_type};VALUE {self._device.rf_lvl_val};INC {self._device.rf_lvl_inc};{self._device.rf_lvl_status} '
	
    def get_modulation(self):
        return f':MODE {self._device.modulation_mode}'
        
    def set_modulation(self, mode):
        self._device.modulation_mode = mode
        return ''

    def get_modulation_control(self):
        return f':MOD:{self._device.modulation_control}'

    def set_modulation_control(self, onoff):
        self._device.modulation_control = onoff
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

    def set_rf_on(self):
        self._device.rf_lvl_status = 'ON'

        return ''

    def set_rf_off(self):
        self._device.rf_lvl_status = 'OFF'

        return ''

    def get_pulse_modulation(self):
        return f':PULSE:ON'
        
    def get_pulse_cw(self):
        return f':PULSE:CAL:ENABLE'

    def get_fm_modulation(self, i):
        return f':FM{i}:DEVN 100.0;INTF;ON;INC 10.0';

    def get_pm_modulation(self, i):
        return f':PM{i}:DEVN 100.0;INTF;ON;INC 10.0';

    def get_am_modulation(self, i):
        return f':AM{i}:DEPTH 100.0;INTF;ON;INC 10.0';

    def get_wbfm_modulation(self):
        return f':WBFM:DEVN 100.0;INTF;ON';

