import pytest

import main


@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()


def test_inventory_route_good(app):
    res = app.get('/inventory', headers={'hello': 'world'})
    assert res.status_code == 200

