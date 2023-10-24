import os
import getpass
from flask import Flask
from app.routes import api
from swagger.swagger import swagger_bp

def set_api_credentials():
    if 'CODE_ALREADY_EXECUTED' not in os.environ:
        # Code has not been executed in this session, prompt for API key and secret
        api_key = getpass.getpass(prompt="Enter your Bittrex API key: ")
        api_secret = getpass.getpass(prompt="Enter your Bittrex API secret: ")

        # Set them as environment variables
        os.environ['BITTREX_API_KEY'] = api_key
        os.environ['BITTREX_API_SECRET'] = api_secret

        # Set the flag to indicate that the code has been executed in this session
        os.environ['CODE_ALREADY_EXECUTED'] = '1'

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(swagger_bp)
    return app

if __name__ == '__main__':
    set_api_credentials()
    app = create_app()
    app.run(debug=True)
