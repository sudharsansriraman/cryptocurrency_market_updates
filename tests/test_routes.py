import pytest
import os
import requests
import time
from main import create_app
from unittest.mock import patch


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    os.environ['BITTREX_API_KEY'] = "YOUR_API_KEY"
    os.environ['BITTREX_API_SECRET'] = "YOUR_API_SECRET"
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


# Test retrieving all market summaries, expects a list in the response
def test_get_all_market_summaries(client):
    response = client.get('/market_summaries')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


# Test for a specific market summary, expects a dictionary
def test_get_market_summary(client):
    response = client.get('/market_summary/ltc-btc')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)


# Test for a missing parameter, expects a 404 response
def test_get_market_summary_missing_param(client):
    response = client.get('/market_summary/')
    assert response.status_code == 404


# Test for an invalid market symbol, expects 'MARKET_DOES_NOT_EXIST'
def test_get_market_summary_invalid_symbol(client):
    response = client.get('/market_summary/invalid-symbol')
    data = response.get_json()
    assert "MARKET_DOES_NOT_EXIST" in data.get("code")


# Test for a missing API key, expects 'APIKEY_INVALID' in the response
def test_get_market_summary_missing_api_key(client):
    with patch.dict(os.environ, {'BITTREX_API_KEY': ''}):
        time.sleep(5)
        response = client.get('/market_summary/ltc-btc')
        data = response.get_json()
        assert "APIKEY_INVALID" in data.get("code")


# Test for a missing API secret, expects 'INVALID_SIGNATURE' in the response
def test_get_market_summary_missing_api_secret(client):
    with patch.dict(os.environ, {'BITTREX_API_SECRET': ''}):
        time.sleep(5)
        response = client.get('/market_summary/ltc-btc')
        data = response.get_json()
        assert "INVALID_SIGNATURE" in data.get("code")


# Test for network failure, expects a 500 response with an 'error'
def test_get_market_summary_network_failure(client):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network failure")
        response = client.get('/market_summary/ltc-btc')
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data


# Test to validate the interaction with the Bittrex API,
# checking for a specific field in the API response.
def test_integration_get_market_summary(client):
    response = client.get('/market_summary/ltc-btc')
    assert response.status_code == 200
    data = response.get_json()
    assert 'volume' in data
