from flask import Blueprint, jsonify
import requests
from config import BITTREX_API_BASE_URL, BITTREX_API_KEY, BITTREX_API_SECRET
import hashlib
import hmac
import time

api = Blueprint('api', __name__)

def generate_bittrex_headers(method, uri, content="", subaccount_id=""):
    timestamp = str(int(time.time() * 1000))
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