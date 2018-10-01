from flask import Flask, request, Blueprint, current_app, jsonify, abort, redirect, session
from fhirclient import client
import fhirclient.models.patient as patient_model
import json
import requests
import secrets
import urllib.parse as urlparse
from cstr import fhir_config

root_api = Blueprint('root_api', __name__, url_prefix='/api')



# Endpoint: /api/test
@root_api.route('/test')
def test():
    """Test endpoint to validate requests can be made to Flask.
    """
    return jsonify({"value": "Hello World"})

@root_api.route('/authorize', methods=['GET'])
def receive_token():
    if request.method != 'GET':
        return abort(404)
    request.args.get('state')
    if request.args.get('state') != session.pop('state'):
        return abort(500)
    request.args.get('code')


@root_api.route('/get_token', methods=['GET'])
def receive_launch_id():
    fhir_client = client.FHIRClient(settings=fhir_config)
    session['state'] = secrets.token_urlsafe(16)
    code_response = requests.get("http://smartonfhir.aehrc.com:8080/oauth/authorize", params={
        "response_type": "code",
        "client_id": "CSTR",
        "redirect_uri": "cstr.uqcloud.net",
        "launch": request.args.get('launch'),
        "scope": "patient/*.*",
        "state": session['state'],
        "aud": request.args.get('iss')
    })
    assert code_response.status_code == 302
    token_url = code_response.headers["Location"]
    token_queries = urlparse.parse_qs(token_url)
    if token_queries['state'] != session.pop('state'):
        return abort(500)
    token_response = requests.post("http://smartonfhir.aehrc.com:8080/oauth/token",
        params={
            "grant_type": "authorization_code",
            "code": token_queries['code'],
            "redirect_uri": "cstr.uqcloud.net",
            "client_id": "CSTR"
        }
    )
    session['token_response'] = token_response.json()
    return '', 200

# Endpoint: /api/patient/<patient_id>
@root_api.route('/patient/<string:patient_id>', methods=['GET'])
def get_patient_history(patient_id: str):
    """Endpoint to get patient info from Smart on FHIR server

    @Return: A json file of the request 
    """
    if session['token_response'] is None:
        receive_launch_id()
    urlparse
    requests.get("http://smartonfhir.aehrc.com:8085/fhir")

def read_json(json_request_return):
    """Function to read JSON given from GET request from FHIR server.

    @Param: takes a json request
    @Return: Dictionary of decoded json
    """
    if json_request_return is not None:
        return json.loads(json_request_return)
