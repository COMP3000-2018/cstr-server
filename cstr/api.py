from flask import Flask, request, Blueprint, jsonify, abort, redirect, session, Response, current_app
import requests
import urllib.parse
import secrets
import json
import os
from cstr import fhir_config


root_api = Blueprint('root_api', __name__, url_prefix='/api')


# Endpoint: /api/test
@root_api.route('/test')
def test():
    """Test endpoint to validate requests can be made to Flask.
    """
    return jsonify({"value": "Hello World"})

@root_api.route('/active_login')
def active_login():
    """Test whether the current user is logged in.
    """
    if 'token' not in session:
        return Response(json.dumps({"status": "Not Authenticated"}), 401, mimetype="application/json")
    else:
        return Response(json.dumps({"status": "Authenticated"}), 200, mimetype="application/json")


@root_api.route('/retrieve_token')
def receive_token():
    if request.args.get('code') is None:
        return abort(400)
    #if request.args.get('state') != session.pop('state'):
    #    return abort(500)
    params = {
        "grant_type": "authorization_code",
        "code": request.args.get('code'),
        "redirect_uri": current_app.config['DOMAIN'],
        "client_id": "CSTR"
    }
    response = requests.post(url="http://smartonfhir.aehrc.com:8080/oauth/token", data=params)
    session['state'] = None
    return Response(response.text, status=200, mimetype="application/json")


@root_api.route('/standalone_launch', methods=['GET'])
def standalone_launch():
    session['state'] = secrets.token_urlsafe(16)
    params = {
        "response_type": "code",
        "client_id": "CSTR",
        "redirect_uri": current_app.config['DOMAIN'],
        "scope": "system/*.*",
        "state": session['state'],
        "aud": "http://smartonfhir.aehrc.com:8085/fhir"
    }
    param_string = "&".join([key + "=" + urllib.parse.quote(params[key], safe="") for key in params])
    ehr_url = urllib.parse.urlunparse(('http', 'smartonfhir.aehrc.com:8080', '/oauth/authorize', None, param_string, ''))
    return Response(json.dumps({"sso_redirect": ehr_url}), status=200, mimetype="application/json")


@root_api.route('/ehr_launch', methods=['GET'])
def ehr_launch():
    if not request.args.get('launch') or not request.args.get('iss'):
        abort(400)
    session['state'] = secrets.token_urlsafe(16)
    params = {
        "response_type": "code",
        "client_id": "CSTR",
        "redirect_uri": current_app.config['DOMAIN'],
        "launch": request.args.get('launch'),
        "scope": "system/*.*",
        "state": session['state'],
        "aud": request.args.get('iss')
    }
    param_string = "&".join([key + "=" + urllib.parse.quote(params[key], safe="") for key in params])
    ehr_url = urllib.parse.urlunparse(('http', 'smartonfhir.aehrc.com:8080', '/oauth/authorize', None, param_string, ''))
    return Response(json.dumps({"sso_redirect": ehr_url}), status=200, mimetype="application/json")


@root_api.route("/patient", methods=['POST'])
def create_patient():
    """

    """
    body = request.get_json(silent=True)
    if not request.args.get("token") or body is None:
        abort(400)

    dict_headers = {
        "Authorization":"Bearer "+ request.args.get('token'),
        "Content-Type": "application/fhir+json"
    }
    server_response = requests.post("http://smartonfhir.aehrc.com:8085/fhir/Patient/", request.get_data(as_text=True),
                                    headers=dict_headers)
    server_parse = json.loads(server_response.text)
    return jsonify(server_parse)


# Endpoint: /api/patient/<patient_id>
@root_api.route('/patient/<string:patient_id>', methods=['GET'])
def get_patient_history(patient_id):
    """Endpoint to get patient info from Smart on FHIR server

    @Return: A json file of the request
    """
    if session['token'] is None:
        abort(401)
    dict_headers = {"Authorization":"Bearer "+json.loads(session['token'])['access_token']}
    patient_info = requests.get("http://smartonfhir.aehrc.com:8085/fhir/Patient/" +
                                urllib.parse.quote(patient_id, safe=""), headers=dict_headers)
    test = json.loads(patient_info.text)
    return jsonify(test)

# Endpoint: /api/Observation/<patient_id>
# @root_api.route('/Observation/<string:patient_id>', methods=['GET', 'POST'])
# def get_patients_observations(patient_id):
#     if request.method == 'POST':
#         """Endpoint to get and post patient's observation info from Smart on FHIR server

#         @Return: A json file of the request
#         """
#         if session['token'] is None:
#             abort(401)

#         #dict_headers = {"Authorization":"Bearer "+json.loads(session['token'])['access_token']}
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization':"Bearer "+json.loads(session['token'])['access_token'],
#         }
#         params = {
#             'access_token': access_token,
#         }
#         payload = {
#             'recipient': {
#                 'id': user_id,
#             },
#             'message': message_data,
#         }
        
#         url = 'http://smartonfhir.aehrc.com:8085/fhir/Observation'
#         response = requests.post(url, headers=headers, params=params,
#                                 data=json.dumps(payload))
#         response.raise_for_status()
#         return response.json()
#     elif request.method == '':
#         if session['token'] is None:
#             abort(401)
#         dict_headers = {"Authorization":"Bearer "+json.loads(session['token'])['access_token']}
#         patient_info = requests.get("http://smartonfhir.aehrc.com:8085/fhir/Observation/" + urllib.parse.quote(patient_id, safe=""),headers=dict_headers)
#         test = json.loads(patient_info.text)
#         return jsonify(test)

# Endpoint: /api/Observation/<patient_id>
@root_api.route('/Observation/<string:patient_id>', methods=['GET'])
def get_observations(patient_id):
    """Endpoint to get Observations of patients from Smart on FHIR server

    @Return: A json file of the request
    """
    if session['token'] is None:
        abort(401)
    dict_headers_observation = {"Authorization":"Bearer "+json.loads(session['token'])['access_token']}
    patient_observation_info = requests.get("http://smartonfhir.aehrc.com:8085/fhir/Observation/" +
                                            urllib.parse.quote(patient_id, safe=""), headers=dict_headers_observation)
    request_result_observation = json.loads(patient_observation_info.text)
    return jsonify(request_result_observation)


# Endpoint: /api/medication/<MEDI7212-medication_name>
# Example: /api/Medication/MEDI7212-Morphine
@root_api.route('/Medication/<string:medication_name>', methods=['GET'])
def get_medication(medication_id):
    """Endpoint to get medication info from Smart on FHIR server

    @Return: A json file of the request
    """
    if session['token'] is None:
        abort(401)
    dict_headers_medication = {"Authorization":"Bearer "+json.loads(session['token'])['access_token']}
    medication_info = requests.get("http://smartonfhir.aehrc.com:8085/fhir/Medication/" + urllib.parse.quote(medication_id, safe=""),headers=dict_headers_medication)
    test = json.loads(medication_info.text)
    return jsonify(test)
