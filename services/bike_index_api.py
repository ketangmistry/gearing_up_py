import requests


BIKE_INDEX_ENDPOINT = 'https://bikeindex.org:443/api/v3/'


def get_manufacturer_by_name(name: str):
    """Gets the manufacturer details from Bike Index API

    Args:
        name (str): manufacturer name

    Returns:
        json: Tuple[int, json]
    """
    resource = 'manufacturers'
    response = requests.get(BIKE_INDEX_ENDPOINT + resource + '/' + name)
    status_code = response.status_code
    payload = response.json()
    return status_code, payload
