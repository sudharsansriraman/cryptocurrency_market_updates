import os
import pytz
import hmac
import hashlib
import requests
from flask import Blueprint, jsonify
from config import BITTREX_API_BASE_URL
from datetime import datetime

# Create a Flask Blueprint for this API
api = Blueprint('api', __name__)


# Function to get the current UTC timestamp in milliseconds
def get_utc_timestamp_milliseconds():
    utc_time = datetime.now(pytz.UTC)
    timestamp_seconds = (utc_time - datetime(
        1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    timestamp_milliseconds = int(timestamp_seconds * 1000)
    return timestamp_milliseconds


# Function to generate API headers for Bittrex requests
def generate_bittrex_headers(method, uri, content="", subaccount_id=""):
    BITTREX_API_KEY = os.environ.get('BITTREX_API_KEY')
    BITTREX_API_SECRET = os.environ.get('BITTREX_API_SECRET')
    timestamp = str(get_utc_timestamp_milliseconds())
    content_hash = hashlib.sha512(content.encode('utf-8')).hexdigest()
    pre_sign = f"{timestamp}{uri}{method}{content_hash}{subaccount_id}"
    signature = hmac.new(BITTREX_API_SECRET.encode('utf-8'),
                         pre_sign.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {
        'Api-Key': BITTREX_API_KEY,
        'Api-Content-Hash': content_hash,
        'Api-Timestamp': timestamp,
        'Api-Signature': signature,
        'Content-Type': 'application/json'
    }
    if subaccount_id:
        headers['Api-Subaccount-Id'] = subaccount_id
    return headers


# Define a route to get all market summaries
@api.route('/market_summaries', methods=['GET'])
def get_all_market_summaries():
    url = f"{BITTREX_API_BASE_URL}/markets/summaries"
    headers = generate_bittrex_headers("GET", uri=url)
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Define a route to get the market summary for a specific market
@api.route('/market_summary/<market>', methods=['GET'])
def get_market_summary(market):
    market_symbol = market
    url = f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary"
    headers = generate_bittrex_headers("GET", uri=url)
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
