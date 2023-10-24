from flask import Blueprint, jsonify
from flask_restx import Api, Resource
from config import BITTREX_API_BASE_URL
import requests
import hashlib
import hmac
from datetime import datetime
import pytz
import os

# Create a Blueprint for Swagger
swagger_bp = Blueprint('swagger', __name__)

# Create an API object for Swagger
api = Api(
    swagger_bp,
    version='1.0',
    title='Bittrex API',
    description='API for accessing Bittrex market data',
    doc='/swagger-ui', # The URL for Swagger UI
)

# Create a namespace for your routes
main_ns = api.namespace('main', description='Main API operations')

@api.route('/market_summaries', methods=['GET'])
class MarketSummaries(Resource):
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self):
        url = f"{BITTREX_API_BASE_URL}/markets/summaries"
        headers = generate_bittrex_headers("GET", uri=url)
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data, 200
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}, 500

@api.route('/market_summary/<market>', methods=['GET'])
class MarketSummary(Resource):
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self, market):
        market_symbol = market
        url = f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary"
        headers = generate_bittrex_headers("GET", uri=url)
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data, 200
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}, 500

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

if __name__ == '__main__':
    with swagger_bp.app.app_context():
        api.init_app(swagger_bp.app)