from collections import OrderedDict

from lewis.devices import StateMachineDevice

from .states import DefaultState, State


class SimulatedAeroflex(StateMachineDevice):
    def _initialize_data(self) -> None:
        """
        Initialize all of the device's attributes.
        """
        self.carrier_freq_val = 2.0
        self.carrier_freq_mode = "FIXED"
        self.carrier_freq_inc = 2
        self.rf_lvl_unit = "DBM"
        self.rf_lvl_type = "EMF"
        self.rf_lvl_val = 30.0
        self.rf_lvl_inc = 3
        self.rf_lvl_status = "ON"
        self.modulation_mode = "PM1"
        self.modulation_control = "ON"
        self.connected = True
        self.triggered = False
        self.error = "100, I AM ERROR"

    def _get_state_handlers(self) -> dict[str, State]:
        return {
            "default": DefaultState(),
        }

    def _get_initial_state(self) -> str:
        return "default"

    def _get_transition_handlers(self) -> OrderedDict:
        return OrderedDict([])
