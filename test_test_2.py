import pytest
import requests
import requests_mock
from test_2 import read_csv_rows, format_rows, get_court_info_with_api, Error


def test_format_to_dict():
    fake_row = [['Iriquois Pliskin', 'SE17TP', 'Crown Court']]
    assert format_rows(fake_row) == [
        {'name': 'Iriquois Pliskin', 'home_postcode': 'SE17TP', 'type_of_court_desired': 'Crown Court'}]


class TestGetCourtsInfoWithAPI:
    """Contains tests of the get_court_info_with_api function."""

    def test_raises_404_error(self, requests_mock):
        """Checks that function raises the correct error upon a 404 response."""
        requests_mock.get(
            f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode=test", status_code=404)
        with pytest.raises(Error) as exception:
            get_court_info_with_api("test", "test2")

        assert exception.value.message == "Unable to match postcode."
        assert exception.value.code == 404

    def test_raises_500_error(self, requests_mock):
        """Checks that function raises the correct error upon a 500 response."""
        requests_mock.get(
            f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode=test", status_code=500)
        with pytest.raises(Error) as exception:
            get_court_info_with_api("test", "test2")

        assert exception.value.message == "Unable to connect to the server."
        assert exception.value.code == 500

    def test_weather_for_location(self, requests_mock):
        """Checks that the weather and temperature returned from the
        load_weather_for_location function is correct"""
        postcode = "IG58JA"
        type_of_court_desired = "Tribunal"
        court = [{"name": "Court",
                 "distance": 0.58,
                  "dx_number": "21 Fake Street",
                  "types": "Tribunal"}]
        requests_mock.get(
            f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}", status_code=200, json=court)
        result = get_court_info_with_api(postcode, type_of_court_desired)
        court_name = court[0]["name"]
        court_distance = court[0]["distance"]
        court_dx_number = court[0]["dx_number"]
        assert result == {"court_name": court_name,
                          "distance": court_distance, "dx_number": court_dx_number}
