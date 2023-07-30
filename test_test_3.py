import pytest
from test_3 import sum_current_time


def test_is_string():
    """Tests if the input to sum_current_time function is something
    other than a string, a TypeError is raised with the correct message"""
    with pytest.raises(TypeError) as err:
        sum_current_time(3)
    assert "This is not a string" in str(err)


def test_is_correct_sum():
    """Tests that the correct number is output from the function
    upon a fake time being provided"""
    fake_time = "01:02:03"
    assert sum_current_time(fake_time) == 6


def test_is_incorrect_hours():
    """Tests that a ValueError is raised with the correct message 
    from the function upon the wrong hours being provided"""
    with pytest.raises(ValueError) as err:
        sum_current_time("60:02:03")
    assert "This is not a valid number of hours" in str(err)


def test_is_incorrect_minutes():
    """Tests that a ValueError is raised with the correct message 
    from the function upon the wrong minutes being provided"""
    with pytest.raises(ValueError) as err:
        sum_current_time("01:99:03")
    assert "This is not a valid number of minutes" in str(err)


def test_is_incorrect_seconds():
    """Tests that a ValueError is raised with the correct message 
    from the function upon the wrong seconds being provided"""
    with pytest.raises(ValueError) as err:
        sum_current_time("01:02:99")
    assert "This is not a valid number of seconds" in str(err)


def test_invalid_string():
    """Tests that a ValueError is raised with the correct message 
    from the function upon the wrong string being provided"""
    with pytest.raises(ValueError) as err:
        sum_current_time("AA:BB:CC")
    assert "The date must be numbers" in str(err)
