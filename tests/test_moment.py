# This file is essentially copied from the main grist repo.


from datetime import datetime, date, timedelta
import pytest
from grist import moment

@pytest.fixture
def fmt():
    return "%Y-%m-%d %H:%M:%S %Z"

@pytest.fixture
def new_york():
    return [
        [datetime(1918, 3, 31, 6, 59, 59), -1633280401000, "EST", 300, 1, 59],
        [datetime(1918, 3, 31, 7, 0, 0), -1633280400000, "EDT", 240, 3, 0],
        [datetime(1918, 10, 27, 5, 59, 59), -1615140001000, "EDT", 240, 1, 59],
        [datetime(1918, 10, 27, 6, 0, 0), -1615140000000, "EST", 300, 1, 0],
        [datetime(1979, 4, 29, 6, 59, 59), 294217199000, "EST", 300, 1, 59],
        [datetime(1979, 4, 29, 7, 0, 0), 294217200000, "EDT", 240, 3, 0],
        [datetime(1979, 10, 28, 5, 59, 59), 309938399000, "EDT", 240, 1, 59],
        [datetime(1979, 10, 28, 6, 0, 0), 309938400000, "EST", 300, 1, 0],
        [datetime(2037, 3, 8, 6, 59, 59), 2120108399000, "EST", 300, 1, 59],
        [datetime(2037, 3, 8, 7, 0, 0), 2120108400000, "EDT", 240, 3, 0],
        [datetime(2037, 11, 1, 5, 59, 59), 2140667999000, "EDT", 240, 1, 59],
    ]

@pytest.fixture
def new_york_errors():
    return [
        ["America/New_York", "2037-3-8 6:59:59", TypeError],
        ["America/New_York", [2037, 3, 8, 6, 59, 59], TypeError],
        ["America/new_york", datetime(1979, 4, 29, 6, 59, 59), KeyError],
    ]

@pytest.fixture
def los_angeles():
    return [
        [datetime(1918, 3, 31, 1, 59, 59, 0), -1633269601000, "PST", 480, 1, 59],
        [datetime(1918, 3, 31, 2, 0, 0, 0), -1633273200000, "PST", 480, 1, 0],
        [datetime(1918, 3, 31, 2, 59, 59, 0), -1633269601000, "PST", 480, 1, 59],
        [datetime(1918, 3, 31, 3, 0, 0, 0), -1633269600000, "PDT", 420, 3, 0],
        [datetime(1918, 10, 27, 0, 59, 59, 0), -1615132801000, "PDT", 420, 0, 59],
        [datetime(1918, 10, 27, 1, 0, 0, 0), -1615132800000, "PDT", 420, 1, 0],
        [datetime(1918, 10, 27, 1, 59, 59, 0), -1615129201000, "PDT", 420, 1, 59],
        [datetime(1918, 10, 27, 2, 0, 0, 0), -1615125600000, "PST", 480, 2, 0],
        [datetime(2008, 3, 9, 1, 59, 59, 0), 1205056799000, "PST", 480, 1, 59],
        [datetime(2008, 3, 9, 2, 0, 0, 0), 1205053200000, "PST", 480, 1, 0],
        [datetime(2008, 3, 9, 2, 59, 59, 0), 1205056799000, "PST", 480, 1, 59],
        [datetime(2008, 3, 9, 3, 0, 0, 0), 1205056800000, "PDT", 420, 3, 0],
        [datetime(2008, 11, 2, 0, 59, 59, 0), 1225612799000, "PDT", 420, 0, 59],
        [datetime(2008, 11, 2, 1, 0, 0, 0), 1225612800000, "PDT", 420, 1, 0],
        [datetime(2008, 11, 2, 1, 59, 59, 0), 1225616399000, "PDT", 420, 1, 59],
        [datetime(2008, 11, 2, 2, 0, 0, 0), 1225620000000, "PST", 480, 2, 0],
        [datetime(2037, 3, 8, 1, 59, 59, 0), 2120119199000, "PST", 480, 1, 59],
        [datetime(2037, 3, 8, 2, 0, 0, 0), 2120115600000, "PST", 480, 1, 0],
        [datetime(2037, 11, 1, 0, 59, 59, 0), 2140675199000, "PDT", 420, 0, 59],
        [datetime(2037, 11, 1, 1, 0, 0, 0), 2140675200000, "PDT", 420, 1, 0],
    ]

def assert_matches(data_entry, moment_obj):
    date_val, timestamp, abbr, offset, hour, minute = data_entry
    dt = moment_obj.datetime()
    assert moment_obj.timestamp == timestamp
    assert moment_obj.zoneAbbr() == abbr
    assert moment_obj.zoneOffset() == timedelta(minutes=-offset)
    assert dt.hour == hour
    assert dt.minute == minute

def test_standard_entry(new_york, new_york_errors):
    name = "America/New_York"
    data = new_york
    for entry in data:
        date_val = entry[0]
        timestamp = entry[1]
        m = moment.tz(date_val).tz(name)
        mts = moment.tz(timestamp, name)
        assert_matches(entry, m)
        assert_matches(entry, mts)
    error_data = new_york_errors
    for entry in error_data:
        name = entry[0]
        date_val = entry[1]
        error = entry[2]
        with pytest.raises(error):
            moment.tz(date_val, name)

def test_zone_entry(los_angeles):
    name = "America/Los_Angeles"
    data = los_angeles
    for entry in data:
        date_val = entry[0]
        timestamp = entry[1]
        m = moment.tz(date_val, name)
        assert_matches(entry, m)

def test_zone(new_york):
    name = "America/New_York"
    tzinfo = moment.tzinfo(name)
    data = new_york
    for entry in data:
        date_val = entry[0]
        ts = entry[1]
        abbr = entry[2]
        offset = entry[3]
        dt = moment.tz(ts, name).datetime()
        assert dt.tzname() == abbr
        assert dt.utcoffset() == timedelta(minutes=-offset)

def test_ts_to_dt():
    value_sec = 1426291200  # 2015-03-14 00:00:00 in UTC
    value_dt_utc = moment.ts_to_dt(value_sec, moment.get_zone("UTC"))
    value_dt_aware = moment.ts_to_dt(value_sec, moment.get_zone("America/New_York"))
    assert value_dt_utc.strftime("%Y-%m-%d %H:%M:%S %Z") == "2015-03-14 00:00:00 UTC"
    assert value_dt_aware.strftime("%Y-%m-%d %H:%M:%S %Z") == "2015-03-13 20:00:00 EDT"

def test_dst_switches(fmt):
    dst_before = -1633280401
    dst_begin = -1633280400
    dst_end = -1615140001
    dst_after = -1615140000
    def ts_to_dt_utc(dt):
        return moment.ts_to_dt(dt, moment.get_zone("UTC"))
    assert ts_to_dt_utc(dst_before).strftime(fmt) == "1918-03-31 06:59:59 UTC"
    assert ts_to_dt_utc(dst_begin).strftime(fmt) == "1918-03-31 07:00:00 UTC"
    assert ts_to_dt_utc(dst_end).strftime(fmt) == "1918-10-27 05:59:59 UTC"
    assert ts_to_dt_utc(dst_after).strftime(fmt) == "1918-10-27 06:00:00 UTC"
    def ts_to_dt_nyc(dt):
        return moment.ts_to_dt(dt, moment.get_zone("America/New_York"))
    assert ts_to_dt_nyc(dst_before).strftime(fmt) == "1918-03-31 01:59:59 EST"
    assert ts_to_dt_nyc(dst_begin).strftime(fmt) == "1918-03-31 03:00:00 EDT"
    assert ts_to_dt_nyc(dst_end).strftime(fmt) == "1918-10-27 01:59:59 EDT"
    assert ts_to_dt_nyc(dst_after).strftime(fmt) == "1918-10-27 01:00:00 EST"
    assert ts_to_dt_nyc(dst_after + 3599).strftime(fmt) == "1918-10-27 01:59:59 EST"

def test_tzinfo(fmt):
    ts1 = 294217199000  # In EST
    ts2 = 294217200000  # In EDT (spring forward, we skip ahead by 1 hour)
    utc_dt1 = datetime(1979, 4, 29, 6, 59, 59)
    utc_dt2 = datetime(1979, 4, 29, 7, 0, 0)
    assert moment.tz(ts1).datetime().strftime(fmt) == "1979-04-29 06:59:59 UTC"
    assert moment.tz(ts2).datetime().strftime(fmt) == "1979-04-29 07:00:00 UTC"
    nyc_dt1 = moment.tz(ts1, "America/New_York").datetime()
    nyc_dt2 = moment.tz(ts2, "America/New_York").datetime()
    assert nyc_dt1.strftime(fmt) == "1979-04-29 01:59:59 EST"
    assert nyc_dt2.strftime(fmt) == "1979-04-29 03:00:00 EDT"
    assert moment.dt_to_ts(nyc_dt1) * 1000 == ts1
    assert moment.dt_to_ts(nyc_dt2) * 1000 == ts2
    assert nyc_dt1 + timedelta(seconds=3601) == nyc_dt2
    assert nyc_dt2 - timedelta(seconds=3601) == nyc_dt1
    assert (nyc_dt1 + timedelta(seconds=3601)).strftime(fmt) == "1979-04-29 03:00:00 EDT"
    assert (nyc_dt2 - timedelta(seconds=3601)).strftime(fmt) == "1979-04-29 01:59:59 EST"

def test_dt_to_ds(fmt):
    value_dt = datetime(2015, 3, 14, 0, 0)  # In UTC
    value_sec = 1426291200
    tzla = moment.get_zone("America/Los_Angeles")
    def format_utc(ts):
        return moment.ts_to_dt(ts, moment.get_zone("UTC")).strftime(fmt)
    assert value_dt.strftime("%Y-%m-%d %H:%M:%S %Z") == "2015-03-14 00:00:00 "
    assert moment.dt_to_ts(value_dt) == value_sec
    value_dt_utc = value_dt.replace(tzinfo=moment.TZ_UTC)
    assert value_dt_utc.strftime(fmt) == "2015-03-14 00:00:00 UTC"
    assert moment.dt_to_ts(value_dt_utc) == value_sec
    value_dt_aware = moment.ts_to_dt(value_sec, moment.get_zone("America/New_York"))
    assert value_dt_aware.strftime(fmt) == "2015-03-13 20:00:00 EDT"
    assert moment.dt_to_ts(value_dt_aware) == value_sec
    assert format_utc(moment.dt_to_ts(value_dt, tzla)) == "2015-03-14 07:00:00 UTC"
    assert format_utc(moment.dt_to_ts(value_dt_utc, tzla)) == "2015-03-14 00:00:00 UTC"
    assert format_utc(moment.dt_to_ts(value_dt_aware, tzla)) == "2015-03-14 00:00:00 UTC"
    value_dt_aware -= timedelta(days=28)
    assert value_dt_aware.strftime(fmt) == "2015-02-13 20:00:00 EST"

def test_date_to_ts(fmt):
    d = date(2015, 3, 14)
    tzla = moment.get_zone("America/Los_Angeles")
    def format_utc(ts):
        return moment.ts_to_dt(ts, moment.get_zone("UTC")).strftime(fmt)
    assert format_utc(moment.date_to_ts(d)) == "2015-03-14 00:00:00 UTC"
    assert format_utc(moment.date_to_ts(d, tzla)) == "2015-03-14 07:00:00 UTC"
    assert moment.ts_to_dt(moment.date_to_ts(d, tzla), tzla).strftime(fmt) == "2015-03-14 00:00:00 PDT"
