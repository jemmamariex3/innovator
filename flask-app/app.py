# import the Flask class from the flask module
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('../google/api')
print(sys.path)
from google.api.api_python import *
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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjQ4NjM4MywiZXh0Ijp7fSwiaWF0IjoxNTc2NDgyNzgzLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiNGMxMDg4NzItMmY1OS00Y2I5LWE5MTctZDhkNjlkNDg4YTIxIiwibmJmIjoxNTc2NDgyNzgzLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.N0GIQP2ugQuk0Ibec74fdSfdI6Q9IXwbmh674uqcYvh58X3dRX41GS_tIsV2YoRJxeMsq_p4eqIWyDMh3f6wS22u-GW6IVs8jDDyuMKFxXDANhyu_oAiuVjAhsut1KZAjBzAXBeXJSOL7emJJPs2gTt8d64wktCpDJSPDxYyqmOodPJ1tWJb69ZQv9XnC6ES6jayZF0fRuhuCA2d_6Tz-SRZPg39_dEKvJixUCnKDQuOHSVsczOWOOn91ViAG1aypGYOvn3nkZZCstNySTA1ZuggvHoJdC0kHeLW1iJ5S7oOaKHbw9IjbSrjBMEYYKb2LS392LwmvfESBEjgedMemwrbufVf8IVavXReHiOIyd8xXoUXiu1eE-zPYUees93_094EXX9q5az__USVgzejTlGoALLcNFtv_TUqRHAlnH9wgcLz2HxZmUlIZF_BfP2q92MYYVjXp06hT5-BgTRa1j3WwuQWfafW1A3h2Px33dN5Ce9yrJOTC2v96eRydTlMhOXLagj4Q2AAyvj2tBdStYwXuyApTJmlBoCj92vGRy-5Dq6ZGFrKmrzVVnvnkGS0AOPtCzQtODn08ohdulwb5L46EhLupWE1HAURAC_uznG84ok_vkEKkJsOLO8L9DA-AQT0wcCN9cqcLWXdE7Xy0Zcae6RcXzgfrj4nlrcK5NU"
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
                            payload_dict=payload_dict
                        )    
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
            message_array = []     

    assert call.code() == StatusCode.OK
    return jsonify(userText=''.join(message_array))    

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