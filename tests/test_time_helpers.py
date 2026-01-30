import unittest

from scripts.tesla import (
    _fmt_local_hhmm_from_now,
    _fmt_local_timestamp_ms,
    _fmt_age_from_timestamp_ms,
    _fmt_minutes_hhmm,
    _parse_hhmm,
)


class TestTimeHelpers(unittest.TestCase):
    def test_fmt_minutes_hhmm_basic(self):
        self.assertEqual(_fmt_minutes_hhmm(0), "00:00")
        self.assertEqual(_fmt_minutes_hhmm(1), "00:01")
        self.assertEqual(_fmt_minutes_hhmm(60), "01:00")
        self.assertEqual(_fmt_minutes_hhmm(23 * 60 + 59), "23:59")

    def test_fmt_minutes_hhmm_wraps_24h(self):
        # Tesla sometimes uses minutes-from-midnight; be defensive.
        self.assertEqual(_fmt_minutes_hhmm(24 * 60), "00:00")
        self.assertEqual(_fmt_minutes_hhmm(25 * 60 + 5), "01:05")

    def test_fmt_minutes_hhmm_invalid(self):
        self.assertIsNone(_fmt_minutes_hhmm(-1))
        self.assertIsNone(_fmt_minutes_hhmm(""))
        self.assertIsNone(_fmt_minutes_hhmm(None))

    def test_parse_hhmm(self):
        self.assertEqual(_parse_hhmm("00:00"), 0)
        self.assertEqual(_parse_hhmm("01:05"), 65)
        self.assertEqual(_parse_hhmm("23:59"), 23 * 60 + 59)

    def test_parse_hhmm_compact_digits(self):
        self.assertEqual(_parse_hhmm("2330"), 23 * 60 + 30)
        self.assertEqual(_parse_hhmm("0730"), 7 * 60 + 30)
        self.assertEqual(_parse_hhmm("730"), 7 * 60 + 30)

    def test_parse_hhmm_hour_only(self):
        self.assertEqual(_parse_hhmm("7"), 7 * 60)
        self.assertEqual(_parse_hhmm("19"), 19 * 60)

    def test_parse_hhmm_ampm(self):
        self.assertEqual(_parse_hhmm("7am"), 7 * 60)
        self.assertEqual(_parse_hhmm("7pm"), 19 * 60)
        self.assertEqual(_parse_hhmm("12am"), 0)
        self.assertEqual(_parse_hhmm("12pm"), 12 * 60)
        self.assertEqual(_parse_hhmm("7:30pm"), 19 * 60 + 30)
        self.assertEqual(_parse_hhmm("07:30 PM"), 19 * 60 + 30)

    def test_parse_hhmm_strips(self):
        self.assertEqual(_parse_hhmm(" 07:30 "), 7 * 60 + 30)

    def test_parse_hhmm_invalid(self):
        for bad in [
            None,
            "",
            " ",
            "7:30",  # allow single-digit hour with colon
        ]:
            if bad == "7:30":
                self.assertEqual(_parse_hhmm(bad), 7 * 60 + 30)
            else:
                with self.assertRaises(ValueError):
                    _parse_hhmm(bad)

        for bad in ["24:00", "00:60", "-1:00", "ab:cd", "12345", "13pm", "0am"]:
            with self.assertRaises(Exception):
                _parse_hhmm(bad)

    def test_fmt_local_hhmm_from_now(self):
        import datetime as dt

        base = dt.datetime(2026, 1, 1, 20, 0, 0)
        self.assertEqual(_fmt_local_hhmm_from_now(0, now=base), "20:00")
        self.assertEqual(_fmt_local_hhmm_from_now(15, now=base), "20:15")
        self.assertEqual(_fmt_local_hhmm_from_now(60, now=base), "21:00")
        self.assertEqual(_fmt_local_hhmm_from_now(2 * 60 + 5, now=base), "22:05")

    def test_fmt_local_hhmm_from_now_invalid(self):
        self.assertIsNone(_fmt_local_hhmm_from_now(-1))
        self.assertIsNone(_fmt_local_hhmm_from_now(None))
        self.assertIsNone(_fmt_local_hhmm_from_now(""))

    def test_fmt_local_timestamp_ms_utc(self):
        import datetime as dt

        # 2026-01-01 00:00:00 UTC
        ts_ms = int(dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc).timestamp() * 1000)
        self.assertEqual(_fmt_local_timestamp_ms(ts_ms, tz=dt.timezone.utc), "2026-01-01 00:00")

    def test_fmt_local_timestamp_ms_invalid(self):
        self.assertIsNone(_fmt_local_timestamp_ms(None))
        self.assertIsNone(_fmt_local_timestamp_ms(""))
        self.assertIsNone(_fmt_local_timestamp_ms(-1))
        self.assertIsNone(_fmt_local_timestamp_ms(0))

    def test_fmt_age_from_timestamp_ms(self):
        import datetime as dt

        base = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)

        # 5 seconds ago => just now
        ts_ms = int((base - dt.timedelta(seconds=5)).timestamp() * 1000)
        self.assertEqual(_fmt_age_from_timestamp_ms(ts_ms, now=base), "just now")

        # 45 seconds ago
        ts_ms = int((base - dt.timedelta(seconds=45)).timestamp() * 1000)
        self.assertEqual(_fmt_age_from_timestamp_ms(ts_ms, now=base), "45s ago")

        # 9 minutes ago
        ts_ms = int((base - dt.timedelta(minutes=9)).timestamp() * 1000)
        self.assertEqual(_fmt_age_from_timestamp_ms(ts_ms, now=base), "9m ago")

        # 2h 3m ago
        ts_ms = int((base - dt.timedelta(hours=2, minutes=3)).timestamp() * 1000)
        self.assertEqual(_fmt_age_from_timestamp_ms(ts_ms, now=base), "2h 3m ago")

        # 3d 4h ago
        ts_ms = int((base - dt.timedelta(days=3, hours=4)).timestamp() * 1000)
        self.assertEqual(_fmt_age_from_timestamp_ms(ts_ms, now=base), "3d 4h ago")

    def test_fmt_age_from_timestamp_ms_invalid(self):
        self.assertIsNone(_fmt_age_from_timestamp_ms(None))
        self.assertIsNone(_fmt_age_from_timestamp_ms(""))
        self.assertIsNone(_fmt_age_from_timestamp_ms(-1))
        self.assertIsNone(_fmt_age_from_timestamp_ms(0))


if __name__ == "__main__":
    unittest.main()
