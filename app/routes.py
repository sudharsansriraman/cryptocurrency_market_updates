from flask import Blueprint, jsonify
import requests
from config import BITTREX_API_BASE_URL
import hashlib
import hmac
from datetime import datetime
import pytz
import os

api = Blueprint('api', __name__)

def get_utc_timestamp_milliseconds():
    utc_time = datetime.now(pytz.UTC)
    timestamp_seconds = (utc_time - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
    timestamp_milliseconds = int(timestamp_seconds * 1000)
    return timestamp_milliseconds

def generate_bittrex_headers(method, uri, content="", subaccount_id=""):
    BITTREX_API_KEY = os.environ.get('BITTREX_API_KEY')
    BITTREX_API_SECRET = os.environ.get('BITTREX_API_SECRET')

    if BITTREX_API_KEY is None or BITTREX_API_SECRET is None:
        return jsonify({'error': 'API key or secret not found in environment variables'}), 500
    timestamp = str(get_utc_timestamp_milliseconds())
    content_hash = hashlib.sha512(content.encode('utf-8')).hexdigest()
    pre_sign = f"{timestamp}{uri}{method}{content_hash}{subaccount_id}"
    signature = hmac.new(BITTREX_API_SECRET.encode('utf-8'), pre_sign.encode('utf-8'), hashlib.sha512).hexdigest()
    
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