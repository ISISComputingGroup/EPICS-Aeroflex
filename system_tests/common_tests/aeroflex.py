from parameterized import parameterized
from utils.channel_access import ChannelAccess
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim

# Device prefix
DEVICE_PREFIX = "AEROFLEX_01"
EMULATOR_NAME = "aeroflex"


class AeroflexTests(object):
    """
    Tests for the Aeroflex
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc(EMULATOR_NAME, DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_wait_time=0.0)

    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_new_carrier_freq_WHEN_set_carrier_freq_THEN_new_carrier_freq_set(self):
        self.ca.set_pv_value("CARRIER_FREQ:SP", 1100)

        self.ca.assert_that_pv_is("CARRIER_FREQ:RBV", 1100)

    @parameterized.expand([("Value 1", 1), ("Value 2", 2), ("Value 3", 3.33333)])
    def test_GIVEN_new_rf_lvl_WHEN_set_rf_lvl_THEN_new_rf_lvl_set(self, _, value):
        self.ca.set_pv_value("RF_LEVEL:SP", value)

        self.ca.assert_that_pv_is("RF_LEVEL", value)

    @skip_if_recsim("Requires emulator for backdoor access.")
    def test_GIVEN_error_set_THEN_error_returned(self):
        self._lewis.backdoor_set_on_device("error", "I AM ERROR")

        self.ca.assert_that_pv_is("ERROR", "I AM ERROR", timeout=10)

    @skip_if_recsim("Requires emulator for backdoor access.")
    def test_WHEN_rf_set_on_THEN_status_is_on(self):
        self._lewis.backdoor_set_on_device("rf_lvl_status", "OFF")
        self.ca.set_pv_value("RF_LEVEL:STATUS:SP", 1)

        self.ca.assert_that_pv_is("RF_STATUS", "ON")

    @skip_if_recsim("Requires emulator for backdoor access.")
    def test_WHEN_rf_set_on_THEN_status_is_off(self):
        self._lewis.backdoor_set_on_device("rf_lvl_status", "ON")
        self.ca.set_pv_value("RF_LEVEL:STATUS:SP", 0)

        self.ca.assert_that_pv_is("RF_STATUS", "OFF")
