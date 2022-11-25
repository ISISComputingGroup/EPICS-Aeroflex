import sys, os
import unittest

from utils.test_modes import TestModes
from parameterized import parameterized
from utils.ioc_launcher import get_default_ioc_dir, EPICS_TOP
from utils.testing import skip_if_recsim
sys.path.append(os.path.join(EPICS_TOP, "support", "aeroflex", "master", "system_tests", "common_tests"))
from aeroflex import AeroflexTests, DEVICE_PREFIX, EMULATOR_NAME


TEST_MODES = [TestModes.DEVSIM, TestModes.RECSIM]

IOCS = [
    {
        'name': DEVICE_PREFIX,
        'directory': get_default_ioc_dir('aeroflex'),
        'macros': {'DEV_TYPE': '2030'},
        'emulator': EMULATOR_NAME,
        'lewis_protocol': 'model2030',
    },
]


class Aeroflex2030Tests(AeroflexTests, unittest.TestCase):
    '''
    Tests for aeroflex model 2030. Tests inherited from AeroflexTests.
    '''
    
    def setUp(self):
        super(Aeroflex2030Tests, self).setUp()
        
    @parameterized.expand([('Value 1', 'AM'), ('Value 2', 'PM'), ('Value 3', 'FM')])
    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_new_modulation_WHEN_set_modulation_THEN_new_modulation_set(self, _, value):
        self.ca.set_pv_value('MODE:SP_NO_ACTION', value)
        self.ca.assert_that_pv_is('MODE:SP_NO_ACTION', value)
        self.ca.set_pv_value('SEND_MODE_PARAMS.PROC', 1)
        
        self.ca.assert_that_pv_is('MODE', value + '1')

    @parameterized.expand([('Value 1', 'FM'), ('Value 2', 'PM')])
    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_new_modulation_WHEN_set_modulation_with_pulse_THEN_new_modulation_set(self, _, value):
        self.ca.set_pv_value('MODE:SP_NO_ACTION', value)
        self.ca.assert_that_pv_is('MODE:SP_NO_ACTION', value)
        
        self.ca.set_pv_value('PULSE_CHECK:SP', 1)
        self.ca.assert_that_pv_is('PULSE_CHECK:SP', 'Pulse enabled')
        
        self.ca.set_pv_value('SEND_MODE_PARAMS.PROC', 1)
        
        self.ca.assert_that_pv_is('MODE', 'PULSE,' + value + '1')
    
    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_new_modulation_WHEN_set_modulation_with_pulse_incorrectly_THEN_pulse_ignored(self):
        self.ca.set_pv_value('MODE:SP_NO_ACTION', 'FM,AM')
        self.ca.assert_that_pv_is('MODE:SP_NO_ACTION', 'FM,AM')
        
        self.ca.set_pv_value('PULSE_CHECK:SP', 1)
        self.ca.assert_that_pv_is('PULSE_CHECK:SP', 'Pulse enabled')
        
        self.ca.set_pv_value('SEND_MODE_PARAMS.PROC', 1)
        self.ca.assert_that_pv_is('MODE', 'FM1,AM1')
        
    def test_GIVEN_old_modulation_WHEN_new_modulation_set_THEN_new_modulation_is_delayed(self):
        self.ca.set_pv_value('MODE', 'AM1')
        self.ca.assert_that_pv_is('MODE', 'AM1')
        
        self.ca.set_pv_value('MODE:SP_NO_ACTION', 'PM')
        self.ca.assert_that_pv_is('MODE:SP_NO_ACTION', 'PM')
        self.ca.set_pv_value('PULSE_CHECK:SP', 0)
        self.ca.set_pv_value('SEND_MODE_PARAMS.PROC', 1)
        
        self.ca.assert_that_pv_is('MODE', 'AM1')
        
        self.ca.assert_that_pv_is('MODE', 'PM1', 2)
    
    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_reset_THEN_values_are_reset(self):
        self.ca.set_pv_value('RESET', 1)
        self.ca.assert_that_pv_is('RESET', 1)
        
        self.ca.assert_that_pv_is('CARRIER_FREQ', 0)
        self.ca.assert_that_pv_is('RF_LEVEL', 0)
        self.ca.assert_that_pv_is('MODE', 'AM1')
        
    def test_GIVEN_rf_prec_THEN_rf_prec_is_correct(self):
        self.ca.assert_that_pv_is('RF_LEVEL.PREC', 2)
        self.ca.assert_that_pv_is('RF_LEVEL:SP.PREC', 2)
        self.ca.assert_that_pv_is('RF_LEVEL:SP_NO_ACTION.PREC', 2)
