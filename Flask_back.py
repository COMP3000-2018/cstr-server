from flask import Flask, request

app = Flask(__name__)

@app.route('/Patient/jim/')
def get_patient_history():
    return request.args.get('patient')

if __name__ == '__main__':
    app.run(debug = True)

