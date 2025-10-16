import utils

def test_duration_to_datetime():
    assert utils.duration_to_datetime(36) == "01j12h00min"

def test_duration_to_datetime_short():
    assert utils.duration_to_datetime_short(32) == "01j08h"

def test_string_duration_to_float_hours():
    assert utils.string_duration_to_float_hours("3j12h30min") == 84.5

def test_convert_seconds_to_hours_minutes():
    assert utils.convert_seconds_to_hours_minutes(7800) == "2h10"

def test_convert_to_24_hours_format():
    assert utils.convert_to_24_hours_format("2025-01-01T15:00:00.0") == "15:00"