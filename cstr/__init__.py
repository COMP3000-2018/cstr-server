from flask import Flask, request, current_app, Blueprint
import os


def create_app(config=None):
    app = Flask(__name__)
    app.config['FHIR_SERVER_URL'] = os.environ.get("FHIR_SERVER_URL")
    app.config['FHIR_AUTH_SERVER_URL'] = os.environ.get("FHIR_AUTH_SERVER_URL")
    from cstr.api import root_api
    app.register_blueprint(root_api)
    return app
