# import the Flask class from the flask module
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('../google/api')
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
modelUrn = "urn:nuance:mix/eng-USA/A174_C517/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjQ3ODQxMCwiZXh0Ijp7fSwiaWF0IjoxNTc2NDc0ODEwLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiMjU2YTcyOTUtYzQyYy00OTY5LWIzYTQtZjczNjAwYjgxNDMyIiwibmJmIjoxNTc2NDc0ODEwLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.VQGpDoT6LpIyC1Hsyx4PHqWGwkB6hpzVgYQ-Kv2-fl16oF6Od_dUK5VUoRnWT8pqiylytoiYiPnnrQqyD854p29Nb0Dfb-Z0tQd9yEepaCZXMQA_sjb_lyz5E93Z530UihaxHT0_iygPnrZHE-QqU1Sf1KsTK1zwdAV_7s5Jxd-8B9VajR-WiTvNdT8WEI66_u7A47mnQQC8xikaJSe8KA3itVBCxyx8708lkXgq5scr2T3YOf4K-qVX7iwmvwzwjnbz61_ZsEy_lXACwLf5klVZSqdv6hqCDzc5jlDDX3jWMRLXaE5CL-vqkOCQqV1G__Cc0p2S_EfN4iCuPgsSoApuf4yZdZu0RJP57PcKfkEN8Fh-KmofRES4qWkAAOckf-Yq9VmlDSGcUXQRLTRTN6mlC6DZ5Wosbj2sd4cJOs9f_ejcrGiCCBjccs6WEnOkdofzUMz21SdZ76K2qSNClHjArqSbaewG1TLtioEjzTFOC9bJwBVDcWQ4suy7WVzjDIhLtuAvPXuSx9qTEADDQndLk2rG8517-pOkU5BHyTb1FntXkUbvQSxuQZILzezap0xdKe9mQvSAAFCk-_2YFs7W3Py2HyoyCHPRuwUijsu005iKgMyxRAeeaL3ryW6Rw644eL3gMBi8qjFlgIL-A9QqIZ1mtkKIaUA3JBWsj4s"
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

def start_chat():
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
    response, call = stop_request(stub, 
                            session_id=session_id
                        )
    assert call.code() == StatusCode.OK
    return jsonify(userText=''.join(message_array))

def continue_chat(): 
    if not request.json:
        abort(400)
    
    payload_dict = {
            "input": request.json
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
    response, call = stop_request(stub, 
                            session_id=session_id
                        )
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