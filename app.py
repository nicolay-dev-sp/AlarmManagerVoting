from urllib import response
import urllib3
import json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

cors = CORS(app)

urlServiceTest = 'https://jsonplaceholder.typicode.com/todos/1'
# urlServiceOne = urlServiceTest
# urlServiceTwo = urlServiceTest
# urlServiceThree = urlServiceTest
urlServiceOne = 'http://127.0.0.1:8100/alarmaprocesada'
urlServiceTwo = 'http://127.0.0.1:8200/alarmaprocesada'
urlServiceThree = 'http://127.0.0.1:8300/alarmaprocesada'
retryHU = True
voteTactic = True
amountOfRetries = 7

@app.route('/sendAlarm')
def sendAlarmRequest():
    response1 = sendAlarm(urlServiceOne)
    response2 = sendAlarm(urlServiceTwo)
    response3 = sendAlarm(urlServiceThree)
    status = compareResult(response1, response2, response3)

    resStatus = 200

    if (status != 'ok'):
        resStatus = 404
        if ((response3 != response1) & (response3 != response2) & (response1 != response2)):
            response = buildResponse(status, '', '{} {} {}'.format(urlServiceOne, urlServiceTwo, urlServiceThree))
        if (response3 == response1 != response2):
            response = buildResponse(status, response3, urlServiceTwo)
        if (response3 != response1 == response2):
            response = buildResponse(status, response1, urlServiceThree)
        if (response1 != response3 == response2):
            response = buildResponse(status, response2, urlServiceOne)
    else:
        response = buildResponse(status, response1, '')
    return json.dumps(response), resStatus

def sendAlarm(url):
    http = urllib3.PoolManager()
    req = http.request('GET', url)
    result = json.loads(req.data)
    # validate the response from alarmManager microservice
    return result

def compareResult(data1, data2, data3):
    if (data1 == data2 == data3):
        status = 'ok'
    else:
        status = 'fail'
    return status

def buildResponse(status, data, serviceFail):
    response = {
        "status": status,
        "data": data,
        "serviceFail": 'none'
    }
    if (status != 'ok'):
        response['serviceFail'] = serviceFail
    return response