"""Test file for test_1.py"""
import pytest
from test_1 import is_log_line, get_dict


def test_line_is_str():
    """Test that checks that the input to is_log_line function is
    a string"""
    with pytest.raises(TypeError) as err:
        is_log_line(1)
    assert "The line is not a string" in str(err)


def test_dict_is_correct():
    """Test that checks that the get_dict function is outputting
    the correct dictionary from the string line input"""
    fake_line = "03/11/21 08:51:01 INFO    :.main: *************** RSVP Agent started ****************"
    assert get_dict(fake_line) == {"timestamp": "03/11/21 08:51:01",
                                   "log_level": "INFO",
                                   "message": ":.main: *************** RSVP Agent started ***************"}
