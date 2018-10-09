from flask import Flask, request, current_app, Blueprint
import os

fhir_config = {
    'app_id': 'cstr',
    'api_base': 'http://smartonfhir.aehrc.com:8085/fhir'
}

def create_app(config=None,config_2=None):
    app = Flask(__name__)
    from cstr.api import root_api
    app.register_blueprint(root_api)
    app.secret_key = os.environ['FLASK_SECRET']
    return app
