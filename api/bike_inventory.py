from data.bikes import get_yaml_object_from_file

from services.bike_index_api import get_manufacturer_by_name

BIKE_INVENTORY_FILE = 'bikes.yaml'


def get() -> list:
    yaml_file = get_yaml_object_from_file(BIKE_INVENTORY_FILE)

    def updater(bike_wrapper):
        bike_index_res = get_manufacturer_by_name(
            bike_wrapper['bike']['manufacturer']
        )
        if bike_index_res['manufacturer']:
            url = bike_index_res['manufacturer']['company_url']
            bike_wrapper['bike']['url'] = url
        return bike_wrapper['bike']

    updates_bikes = [
        updater(bike_wrapper) for bike_wrapper in yaml_file['bikes']
    ]

    return updates_bikes
