import bike_inventory


def test_manufacturer_url_update():
    bikes = bike_inventory.get()
    assert bikes[0]['url'] != 'unknown'
