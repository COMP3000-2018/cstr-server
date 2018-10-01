from flask import Flask, request, Blueprint, current_app, jsonify, abort, redirect, session
from fhirclient import client
import fhirclient.models.patient as patient_model
import json
import requests
import secrets
from cstr import fhir_config

root_api = Blueprint('root_api', __name__, url_prefix='/api')

# Endpoint: /api/test
@root_api.route('/test')
def test():
    """Test endpoint to validate requests can be made to Flask.
    """
    return jsonify({"value": "Hello World"})

@root_api.route('/patient/<string:patient_id>', methods=['GET'])
def receive_token(token: str):
    if request.method != 'GET':
        return abort(404)
    request.args.get('state')
    if request.args.get('state') != session.pop('state'):
        return abort(500)
    request.args.get('code')

# Endpoint: /api/patient/<patient_id>
@root_api.route('/patient/<string:patient_id>', methods=['GET'])
def get_patient_history(patient_id: str):
    """Endpoint to get patient info from Smart on FHIR server

    @Return: A json file of the request 
    """
    if request.method != 'GET':
        return abort(404)
    request.args.get('patient_id')
    fhir_client = client.FHIRClient(settings=fhir_config)
    if request.args.get("launch"):
        session['state'] = secrets.token_urlsafe(16)
        requests.get(fhir_client.authorize_url, {
            "response_type": "code",
            "client_id": fhir_config['app_id'],
            "redirect_uri": "",
            "launch": request.args.get('launch'),
            "scope": "patient/*.*",
            "state": session['state'],
            "aud": fhir_config['api_base']
        })
    elif requests.args.get("code"):

    if not fhir_client.prepare():
        if not request.args.get('launch'):
            return redirect(fhir_client.authorize_url, code=302)

    patient = patient_model.Patient.read('', fhir_client.server)


def read_json(json_request_return):
    """Function to read JSON given from GET request from FHIR server.

    @Param: takes a json request
    @Return: Dictionary of decoded json
    """
    if json_request_return is not None:
        return json.loads(json_request_return)
