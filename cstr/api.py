from flask import Flask, request, Blueprint, current_app, jsonify, abort, redirect
from fhirclient import client
import fhirclient.models.patient as patient_model
import json
from cstr import fhir_config

root_api = Blueprint('root_api', __name__, url_prefix='/api')

# Endpoint: /api/test
@root_api.route('/test')
def test():
    """Test endpoint to validate requests can be made to Flask.
    """
    return jsonify({"value": "Hello World"})


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
    if not fhir_client.prepare():
        return redirect(fhir_client.authorize_url, code=302)
    patient = patient_model.Patient.read('', fhir_client.server)


def read_json(json_request_return):
    """Function to read JSON given from GET request from FHIR server.

    @Param: takes a json request
    @Return: Dictionary of decoded json
    """
    if json_request_return is not None:
        return json.loads(json_request_return)
