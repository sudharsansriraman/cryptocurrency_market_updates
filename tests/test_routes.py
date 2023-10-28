import pytest
import os
import requests
from main import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    os.environ['BITTREX_API_KEY'] = "3987ed44be224a1395704ea96c02901b"
    os.environ['BITTREX_API_SECRET'] = "6ef993a021224086b0d43782a710141c"
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

def test_get_market_summary_invalid_symbol(client):
    response = client.get('/market_summary/invalid-symbol')
    data = response.get_json()
    assert "MARKET_DOES_NOT_EXIST" in data.get("code")

def test_get_market_summary_missing_api_key(client):
    with patch.dict(os.environ, {'BITTREX_API_KEY': ''}):
        response = client.get('/market_summary/ltc-btc')
        data = response.get_json()
        assert "APIKEY_INVALID" in data.get("code")

def test_get_market_summary_missing_api_secret(client):
    with patch.dict(os.environ, {'BITTREX_API_SECRET': ''}):
        response = client.get('/market_summary/ltc-btc')
        data = response.get_json()
        assert "INVALID_SIGNATURE" in data.get("code")

def test_get_market_summary_network_failure(client):
    # Simulate a network failure
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network failure")
        response = client.get('/market_summary/ltc-btc')
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data


def test_integration_get_market_summary(client):
    # This is an integration test to validate the interaction with the Bittrex API
    response = client.get('/market_summary/ltc-btc')
    assert response.status_code == 200
    data = response.get_json()
    assert 'volume' in data  # Check for a specific field in the Bittrex API response
