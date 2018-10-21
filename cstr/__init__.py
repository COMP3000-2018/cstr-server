from flask import Flask, request, current_app, Blueprint
from cstr.settings import *
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
    if 'FLASK_ENV' in os.environ:
        if os.environ['FLASK_ENV'] == 'development':
            app.config.from_object(DevelopmentConfig)
        else:
            app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(ProductionConfig)
    return app
