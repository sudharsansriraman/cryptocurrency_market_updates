import pytest
import main

@pytest.fixture
def app():
    app = main.create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_all_market_summaries(client):
    response = client.get('/market_summaries')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Assuming the response is a list of market summaries

def test_get_market_summary(client):
    response = client.get('/market_summary/ltc-btc')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)  # Assuming the response is a dictionary representing the market summary

def test_get_market_summary_missing_param(client):
    response = client.get('/market_summary/')
    assert response.status_code == 404