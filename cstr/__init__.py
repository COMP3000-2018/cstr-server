from flask import Flask, request

app = None

def create_app(config=None):
    app = Flask(__name__)
    return app

@app.route('/api/patient/jim/')
def get_patient_history():
    return request.args.get('patient')

@app.route('/api/test')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app = create_app()
    app.run(debug = True)
