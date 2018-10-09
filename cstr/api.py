from flask import Flask, request, Blueprint, jsonify, abort, redirect, session
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

@root_api.route('/authorize')
def receive_token():
    if request.args.get('state') != session.pop('state'):
        return abort(500)
    params = {
        "grant_type": "authorization_code",
        "code": request.args.get('code'),
        "redirect_uri": "http://cstr.uqcloud.net/api/authorize",
        "client_id": "CSTR"
    }
    response = requests.post(url="http://smartonfhir.aehrc.com:8080/oauth/token", data=params)
    session['state'] = None
    session['token'] = response.text
    return jsonify({"message": "Auth token associated to user"})


@root_api.route('/get_token', methods=['GET'])
def receive_launch_id():
    session['state'] = secrets.token_urlsafe(16)
    params = {
        "response_type": "code",
        "client_id": "CSTR",
        "redirect_uri": "http://cstr.uqcloud.net/api/authorize",
        "launch": request.args.get('launch'),
        "scope": "system/*.*",
        "state": session['state'],
        "aud": request.args.get('iss')
    }
    param_string = "&".join([key + "=" + urllib.parse.quote(params[key], safe="") for key in params])
    ehr_url = urllib.parse.urlunparse(('http', 'smartonfhir.aehrc.com:8080', '/oauth/authorize', None, param_string, ''))
    return redirect(ehr_url)
    #return redirect("http://smartonfhir.aehrc.com:8080/oauth/authorize?response_type=code&client_id=CSTR&redirect_uri=cstr.uqcloud.net&launch=" + request.args.get('launch') +
    #    "&scope=patient/*.*&state=" + session['state'] + "&aud=" + request.args.get('iss') )


# Endpoint: /api/patient/<patient_id>
@root_api.route('/Patient/<string:patient_id>', methods=['GET'])
def get_patient_history(patient_id):
    """Endpoint to get patient info from Smart on FHIR server

    @Return: A json file of the request
    """
    if session['token'] is None:
        abort(401)
    dict_headers = {"Authorization":"Bearer "+json.loads(session['token'])['access_token']}
    patient_info = requests.get("http://smartonfhir.aehrc.com:8085/fhir/Patient/" + urllib.parse.quote(patient_id, safe=""),headers=dict_headers)
    test = json.loads(patient_info.text)
    return jsonify(test)

