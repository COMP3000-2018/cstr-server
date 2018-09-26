from flask import Flask, request

app = Flask(__name__)

@app.route('/api/patient/jim/')
def get_patient_history():
    return request.args.get('patient')

@app.route('/api/test')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run(debug = True)

