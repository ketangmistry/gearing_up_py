import pytest

import main


@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()


def test_root_route_good_header(app):
    res = app.get('/', headers={'Content-Type': 'application/json'})
    assert res.status_code == 200


def test_root_route_bad_header(app):
    res = app.get('/', headers={'Content-Type': 'text/html'})
    assert res.status_code == 400
