import urllib3
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eporra.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = 'frase-secreta'
# app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

cors = CORS(app)

@app.route('/sendAlarm')
def sendAlarm():
    http = urllib3.PoolManager()
    req = http.request('GET', 'https://jsonplaceholder.typicode.com/todos/1')
    return req.data