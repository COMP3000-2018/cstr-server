from flask import Flask, request, Blueprint, current_app, jsonify, abort
import requests as external_requests
import json

root_api = Blueprint('root_api', __name__, url_prefix='/api')

#Endpoint: /api/test
@root_api.route('/test')
def test():
    """Test endpoint to validate requests can be made to Flask.
    """
    return jsonify({"value": "Hello World"})


# Endpoint: /api/Patient/<patient_id>
@root_api.route('/Patient/<int:patient_id>', methods=['GET'])
def get_patient_history():
    """Endpoint to get patient info from Smart on FHIR server

    @Return: A json file of the request 
    """
    
    if request.method != 'GET':
        return abort(404)
    request.args.get('patient_id')
    remote = current_app.config['FHIR_SERVER_URL']
    external_requests.get(remote)


def read_json(json_request_return):
    """Function to read JSON given from GET request from FHIR server.

    @Param: takes a json request
    @Return: Dictionary of decoded json
    """
    if json_request_return is not None:
        return json.loads(json_request_return)
