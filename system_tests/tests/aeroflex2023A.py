import os
import sys
import unittest

from parameterized import parameterized
from utils.ioc_launcher import EPICS_TOP, get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import skip_if_recsim

sys.path.append(
    os.path.join(EPICS_TOP, "support", "aeroflex", "master", "system_tests", "common_tests")
)
from aeroflex import DEVICE_PREFIX, EMULATOR_NAME, AeroflexTests

TEST_MODES = [TestModes.DEVSIM, TestModes.RECSIM]

IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("aeroflex"),
        "macros": {"DEV_TYPE": "2023A"},
        "emulator": EMULATOR_NAME,
        "lewis_protocol": "model2023A",
    },
]


class Aeroflex2023ATests(AeroflexTests, unittest.TestCase):
    """
    Tests for aeroflex model 2023A. Tests inherited from AeroflexTests.
    """

    def setUp(self):
        super(Aeroflex2023ATests, self).setUp()

    @parameterized.expand(
        [
            ("Value 1", "AM"),
            ("Value 2", "PM,AM"),
            ("Value 3", "FM,AM,PULSE"),
            ("Value 4", "FSK2L,PULSE"),
        ]
    )
    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_new_modulation_WHEN_set_modulation_THEN_new_modulation_set(self, _, value):
        self.ca.set_pv_value("MODE:SP", value)
        self.ca.assert_that_pv_is("MODE:SP", value)

        self.ca.assert_that_pv_is("MODE", value)

    @parameterized.expand([("Value 1", "FM", ""), ("Value 2", "PM", ""), ("Value 2", "AM", "")])
    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_new_modulation_WHEN_set_modulation_with_pulse_THEN_new_modulation_set(
        self, _, value, pulse
    ):
        pulse = "PULSE"
        self.ca.set_pv_value("MODE:SP", value)
        self.ca.assert_that_pv_is("MODE:SP", value)

        self.ca.set_pv_value("MODE:SP", value + "," + pulse)

        self.ca.assert_that_pv_is("MODE", value + ",PULSE")

    @skip_if_recsim("Requires emulator.")
    def test_GIVEN_reset_THEN_values_are_reset(self):
        self.ca.set_pv_value("RESET", 1)
        self.ca.assert_that_pv_is("RESET", 1)

        self.ca.assert_that_pv_is("CARRIER_FREQ:RBV", 0)
        self.ca.assert_that_pv_is("RF_LEVEL", 0)
        self.ca.assert_that_pv_is("MODE", "AM")

    def test_GIVEN_rf_prec_set_THEN_rf_prec_is_correct(self):
        self.ca.assert_that_pv_is("RF_LEVEL.PREC", 6)
        self.ca.assert_that_pv_is("RF_LEVEL:SP.PREC", 6)
