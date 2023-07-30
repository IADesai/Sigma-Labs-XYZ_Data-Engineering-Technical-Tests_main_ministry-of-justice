import pytest
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

        assert exception.value.message == "Unable to connect to server."
        assert exception.value.code == 500

#     def test_weather_for_location(self, requests_mock):
#         """Checks that the weather and temperature returned from the
#         load_weather_for_location function is correct"""
#         lat = 18.010702
#         lng = -66.563545
#         weather_data = {"current": {"temp_c": "20",
#                                     "condition": {"text": "Windy"}}}
#         requests_mock.get(f"http://api.weatherapi.com/v1/current.json?\
# key=7bce67e74ef44f2595a145120232206&q={lat},{lng}", status_code=200, json=weather_data)
#         result = load_weather_for_location(lat, lng)
#         arrival_weather = weather_data["current"]["condition"]["text"]
#         arrival_temperature = weather_data["current"]["temp_c"]
#         assert result == (arrival_weather, arrival_temperature)
