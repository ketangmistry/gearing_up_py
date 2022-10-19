import json
import requests


BIKE_INDEX_ENDPOINT = 'https://bikeindex.org:443/api/v3/'


def get_manufacturer_by_name(name: str) -> json:
    resource = 'manufacturers'
    response = requests.get(BIKE_INDEX_ENDPOINT + resource + '/' + name)
    payload = response.json()
    return payload
