# import the Flask class from the flask module
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('../google/api')
print(sys.path)
from python_enh.dialog.dlg_client import *
import mimetypes

mimetypes.add_type('text/javascript', '.js')

# create the application object
app = Flask(__name__)
CORS(app)    #CORS origin issue still persists.. Hmmm.

tasks = [
    {
        'id': 1,
        'title': u'Start Chat',
        'description': u'Start Chat Request',
        'done': False
    }

]

# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C598/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjUzMDk4OCwiZXh0Ijp7fSwiaWF0IjoxNTc2NTI3Mzg4LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiOTIxYzFiYjEtMWI0Mi00MWE0LTk1ZWYtZTQ4ZDJiNzc4NjBiIiwibmJmIjoxNTc2NTI3Mzg4LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.Co5WqiDhMiZIo5al1DOTxOfdMt1mdsCtjJ9DbfI6AkbZDJ4Oo1lyBEoSLTT9dmXPZUGxipCX31gkiz6OWVz15Gj3OzxJ7Br2KXZQlhBIqK10rF7mPgAdG_ZmLBr7lsSDCJSsdNtRv-CNET1Q1oPbWbiJedJazZPzDMlPufwrNuYxTjQla9OQxZOD_9_CEmDpQxV-XJ0gbzHkRHYYBOkMtx7H3M95jzrOWo0JtK-UBujejvhzjWfD0JUzemDpjkb1Ca7SUNn-4QF7f0ubSLxqPoGLmnvJBEyFeM9WVAHiaKqsMi4rbMh8RRLZzXbK7UPKK5j1O9CE-8316SKyLMMyz9TqQnbrqrs4u2J7fAQ6wCn_SemviJ9574Yka-Ga4_Pe-BzkbbWOI-k1y2OfL9-kbqDh77T2fMz83Jm1BIzi2hflej__kBMY1fCX3RcnFAeaDZ_nxKWa3lGobfa6qCtQ90BsBT8GMUTu90u937RFpKUr2DTNR3rZMRgBhckxK6jW8At-7iDjIFOpxTfswAi2RJx-h2tEifh3-EZlhUOu92Kp3g60h1qdOF7mrWz29OwYwVHLIEKP8y4PKQ0tsD0HWHbAat4kCf_lAHZoQC-v27mAWr9UMhPYR2st4ztc_60yFWZJH2DwdeXj6ld4NZlk6Hq4BWKrhsk97iK9WDNBgGc"
serverUrl = "dlgaas.beta.mix.nuance.com:443"
textInput = "test"

channel = create_channel(token, serverUrl)
stub = ChannelConnectorServiceStub(channel)
selector_dict = {
            "channel": "smartspeakerva",
            "language": "en-US",
            "library": "default"
}
session_id = ''
data_id = ''
data_values = {}

def start_chat():
    global session_id
    response, call = start_request(stub, 
                            model_ref=modelUrn, 
                            session_id=str(uuid.uuid1()), # Create a session id
                            selector_dict=selector_dict
                        )
    session_id = read_session_id_from_response(response)
    #log.debug(f'Session: {session_id}')
    #assert call.code() == StatusCode.OK
    print("started the request")
    print(response)
    payload_dict = {
            "input": {
                "userText": "Hello"
            }
    }
    response, call = execute_request(stub, 
                            session_id=session_id, 
                            selector_dict=selector_dict,
                            payload_dict=payload_dict
                        )  
    va_response = response["payload"]
    message_array = []
    for prompts in va_response["action"]:
        for message in prompts["prompt"]["visual"]:
            message_array.append(message["text"])
    #response, call = stop_request(stub, session_id=session_id)
    #assert call.code() == StatusCode.OK
    return jsonify(userText=''.join(message_array))

def continue_chat(): 
    global session_id
    global data_id
    global data_values

    if not request.json:
        abort(400)
    payload_dict = {
            "input": request.json
    }
    print(session_id) 
    print("hmmmmmmmMMMMMM")

    response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=data_action
                                )
    va_response = handle_response(response)
    print(va_response)
    assert call.code() == StatusCode.OK
    return jsonify(userText=va_response)
"""
    va_response = response["payload"]
    message_array = []
    for action in va_response["action"]:
        if "prompt" in action:
            for message in action["prompt"]["visual"]:
                message_array.append(message["text"])
        elif "data" in action:
            data_id = action["data"]["id"]
            data_values = action["data"]["value"]
            for value in data_values:
                data_values[value] = 5
            payload_dict = { 
                "value": data_values
            }
            response, call = execute_request(stub, 
                            session_id=session_id, 
                            selector_dict=selector_dict,
                            payload_dict=payload_dict
                        )
            va_response = response["payload"]
            message_array = []"""    

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('index.html') # render a template

@app.route('/chat', methods=['GET', 'POST'])
def chat():
        if request.method == 'GET':
            return start_chat()
        elif request.method == 'POST': 
            return continue_chat()



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)