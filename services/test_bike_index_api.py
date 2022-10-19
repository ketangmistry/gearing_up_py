import bike_index_api


def test_get_known_manufacturer():
    json_payload = bike_index_api.get_manufacturer_by_name('Giant')
    assert json_payload['manufacturer']['name'] == 'Giant (and LIV)'


def test_get_unknown_manufacturer():
    json_payload = bike_index_api.get_manufacturer_by_name('Dummy')
    msg = 'Unable to find manufacturer with name or id: Dummy'
    assert json_payload['error'] == msg
