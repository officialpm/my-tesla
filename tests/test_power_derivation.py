import unittest

import scripts.tesla as tesla


class TestPowerDerivation(unittest.TestCase):
    def test_derive_power_kw_valid(self):
        self.assertAlmostEqual(tesla._derive_power_kw(240, 32), 7.68, places=2)

    def test_derive_power_kw_invalid(self):
        self.assertIsNone(tesla._derive_power_kw(None, 32))
        self.assertIsNone(tesla._derive_power_kw(240, None))
        self.assertIsNone(tesla._derive_power_kw(-1, 10))

    def test_charge_status_json_derives_charger_power_when_missing(self):
        charge = {
            'charger_power': None,
            'charger_voltage': 240,
            'charger_actual_current': 32,
        }
        out = tesla._charge_status_json(charge)
        # Rounded to one decimal in helper.
        self.assertEqual(out.get('charger_power'), 7.7)


if __name__ == '__main__':
    unittest.main()
