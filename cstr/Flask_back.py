from flask import Flask, request
import json

app = Flask(__name__)

"""
Function to grab patients' data through their ID, from the 

@Return: A json file of the request 
"""
@app.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient_history():
    if request.method == 'GET':
        return request.args.get('patient_id')

"""
Function to read JSON given from GET request from FHIR server.

@Param: takes a json request
@Return: Dictionary of decoded json
"""
def read_json(json_request_return):
    if json_request_return is not None:
        return json.loads(json_request_return)

if __name__ == '__main__':
    app.debug = True
    app.run(host='52.65.117.202', port=8092)
