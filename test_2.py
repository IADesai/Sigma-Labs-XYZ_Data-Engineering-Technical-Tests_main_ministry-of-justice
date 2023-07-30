# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type

import csv
import requests
import json


class Error(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code


def read_csv_rows() -> list:
    """Function that reads the csv rows from people.csv and 
    outputs a list of lists where the rows of information 
    are the items in the larger list"""
    rows = []
    with open('people.csv') as file:
        csv_file = csv.reader(file)
        for row in csv_file:
            rows.append(row)
    return rows[1:]


def format_rows(rows: list) -> list:
    """Function that formats the rows of information from lists into
    dictionaries, to specify the sections of data in the rows of 
    information (into name, postcode, and court type)"""
    dict_formatted_rows = []
    for row in rows:
        dict = {}
        dict["name"] = row[0]
        dict["home_postcode"] = row[1]
        dict["type_of_court_desired"] = row[2]
        dict_formatted_rows.append(dict)
    return dict_formatted_rows


def find_distance(court: dict) -> float:
    """Function that takes a court and returns the distance as a float
    to be used as a key for sorting the matched courts"""
    return court["distance"]


def get_court_info_with_api(home_postcode: str, type_of_court_desired: str) -> dict:
    """Function that retrieves and returns relevant court information 
    from the postcode provided for a specific row"""
    response = requests.get(
        f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={home_postcode}")
    if response.status_code == 404:
        raise Error("Unable to match postcode.", 404)
    if response.status_code == 500:
        raise Error("Unable to connect to the server.", 500)
    court_data = json.loads(response.text)
    matching_courts = []
    for court in court_data:
        if type_of_court_desired in court["types"]:
            dict = {}
            dict["court_name"] = court["name"]
            dict["distance"] = court["distance"]
            if court["dx_number"] == None:
                court["dx_number"] = "No dx_number available"
            dict["dx_number"] = court["dx_number"]
            matching_courts.append(dict)
    if matching_courts == []:
        raise Exception("Unable to find any courts of that type nearby")
    matching_courts.sort(key=find_distance)
    closest_court = matching_courts[0]
    return closest_court


def upload_to_csv(dict_formatted_rows: list) -> None:
    """Function that deletes previous runs csv file and then 
    uploads the rows of dictionaries to a csv file as the formatted 
    output data file"""
    with open("output_court_data.csv", "w") as file:
        file.seek(0)
        file.truncate()
        file = csv.DictWriter(file, dict_formatted_rows[0].keys())
        file.writeheader()

    for row in dict_formatted_rows:
        with open("output_court_data.csv", "a") as file:
            file = csv.DictWriter(file, row.keys())
            file.writerow(row)


if __name__ == "__main__":
    # [TODO]: write your answer here
    rows = read_csv_rows()
    dict_formatted_rows = format_rows(rows)
    for row in dict_formatted_rows:
        closest_court = get_court_info_with_api(
            row["home_postcode"], row["type_of_court_desired"])
        row["nearest_court_of_the_right_type"] = closest_court["court_name"]
        row["dx_number"] = closest_court["dx_number"]
        row["distance"] = closest_court["distance"]
    upload_to_csv(dict_formatted_rows)
