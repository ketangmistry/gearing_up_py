import json
import requests


BIKE_INDEX_ENDPOINT = 'https://bikeindex.org:443/api/v3/'


def get_manufacturer_by_name(name: str) -> json:
    """Gets the manufacturer details from Bike Index API

    Args:
        name (str): manufacturer name

    Returns:
        json: JSON payload returned from Bike Index
    """
    resource = 'manufacturers'
    response = requests.get(BIKE_INDEX_ENDPOINT + resource + '/' + name)
    payload = response.json()
    return payload
