from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply
from .aeroflex_base import CommonStreamInterface

__all__ = ["Aeroflex2030StreamInterface"]

if_connected = conditional_reply('connected')

@has_log
class Aeroflex2030StreamInterface(CommonStreamInterface, StreamInterface):
    protocol = 'model2030'
    
    commands = CommonStreamInterface.commands
    in_terminator = CommonStreamInterface.in_terminator
    out_terminator = CommonStreamInterface.out_terminator
    
    def get_carrier_freq(self):
        return f':CFRQ:VALUE {self._device.carrier_freq_val};INC {self._device.carrier_freq_inc}'
        
    def reset(self):
        self._device.carrier_freq_val = 0
        self._device.rf_lvl_val = 0
        self._device.modulation_mode = 'AM1'
        
        return ''
