from flask import Blueprint, jsonify
from config import BITTREX_API_BASE_URL
import requests

api = Blueprint('api', __name__)
    
@api.route('/market_summaries', methods=['GET'])
def get_all_market_summaries():
    url = f"{BITTREX_API_BASE_URL}/markets/summaries"
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@api.route('/market_summary/<market>', methods=['GET'])
def get_market_summary(market):
    market_symbol = market
    url = f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary"
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500