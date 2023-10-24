from flask import Flask
from app.routes import api
from swagger.swagger import swagger_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(swagger_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
