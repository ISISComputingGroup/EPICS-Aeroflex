import unittest

from parameterized import parameterized
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim

DEVICE_PREFIX = 'AEROFLEX_01'
DEVICE_NAME = 'aeroflex'

IOCS = [
    {
        'name': DEVICE_PREFIX,
        'directory': get_default_ioc_dir('aeroflex'),
        'macros': {},
        'emulator': DEVICE_NAME,
    },
]

TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]

class AeroflexTests(unittest.TestCase):
    '''
    Tests for the Aeroflex IOC.
    '''
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc(DEVICE_NAME, DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_wait_time=0.0)

    @skip_if_recsim('Requires emulator logic so not supported in RECSIM')
    def test_GIVEN_new_carrier_freq_WHEN_set_carrier_freq_THEN_new_carrier_freq_set(self):        

        self.ca.set_pv_value('CARRIER_FREQ:SP_NO_ACTION', 1.2)
        self.ca.assert_that_pv_is('CARRIER_FREQ:SP_NO_ACTION', 1.2)
        self.ca.set_pv_value('CARRIER_FREQ_UNITS:SP', 'kHZ')
        self.ca.assert_that_pv_is('CARRIER_FREQ_UNITS:SP', 'kHZ')
        self.ca.set_pv_value('SEND_CAR_FREQ_PARAMS.PROC', 1)
        
        self.ca.assert_that_pv_is('CARRIER_FREQ', 1200)

    @parameterized.expand([('Value 1', 1), ('Value 2', 2), ('Value 3', 3.33333)])
    @skip_if_recsim('Requires emulator logic so not supported in RECSIM')
    def test_GIVEN_new_rf_lvl_WHEN_set_rf_lvl_THEN_new_rf_lvl_set(self, _, value):
        self.ca.set_pv_value('RF_LEVEL:SP_NO_ACTION', value)
        self.ca.assert_that_pv_is('RF_LEVEL:SP_NO_ACTION', value)
        self.ca.set_pv_value('SEND_RF_LVL_PARAMS.PROC', 1)

        self.ca.assert_that_pv_is('RF_LEVEL', value)

    @parameterized.expand([('Value 1', 'AM'), ('Value 2', 'AM,PM'), ('Value 3', 'AM,PM,PULSE')])
    @skip_if_recsim('Requires emulator logic so not supported in RECSIM')
    def test_GIVEN_new_modulation_WHEN_set_modulation_THEN_new_modulation_set(self, _, value):
        self.ca.set_pv_value('MODE:SP_NO_ACTION', value)
        self.ca.assert_that_pv_is('MODE:SP_NO_ACTION', value)
        self.ca.set_pv_value('SEND_MODE_PARAMS.PROC', 1)
        
        self.ca.assert_that_pv_is('MODE', value)
        
    @skip_if_recsim('Requires emulator logic so not supported in RECSIM')
    def test_GIVEN_reset_THEN_values_are_reset(self):
        self.ca.set_pv_value('RESET', 1)
        self.ca.assert_that_pv_is('RESET', 1)
        
        self.ca.assert_that_pv_is('CARRIER_FREQ', 0)
        self.ca.assert_that_pv_is('RF_LEVEL', 0)
        self.ca.assert_that_pv_is('MODE', 'AM')

    @skip_if_recsim('Requires emulator logic so not supported in RECSIM')
    def test_GIVEN_error_set_THEN_error_returned(self):
        self._lewis.backdoor_set_on_device('error', 'I AM ERROR')
        
        self.ca.assert_that_pv_is('ERROR', 'I AM ERROR', timeout=10)
