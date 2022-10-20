import bike_index_api


def test_get_known_manufacturer():
    status_code, json_payload = bike_index_api.get_manufacturer_by_name(
        'Giant'
    )
    assert status_code == 200
    assert json_payload['manufacturer']['name'] == 'Giant (and LIV)'


def test_get_unknown_manufacturer():
    status_code, json_payload = bike_index_api.get_manufacturer_by_name(
        'Dummy'
    )
    msg = 'Unable to find manufacturer with name or id: Dummy'
    assert status_code == 404
    assert json_payload['error'] == msg
