# import the Flask class from the flask module
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sys
sys.path.append('../google/api')
from google.api.api_python import *
import mimetypes

mimetypes.add_type('text/javascript', '.js')

# create the application object
app = Flask(__name__)
CORS(app)    #CORS origin issue still persists.. Hmmm.

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjQ2NjkzMSwiZXh0Ijp7fSwiaWF0IjoxNTc2NDYzMzMxLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiMjE4Mjk5N2EtYmM1YS00Nzg5LTlmZWQtNzhhNTc4YzZkYTg4IiwibmJmIjoxNTc2NDYzMzMxLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.qlvwvpfrPBnEdnlEajHc4hg-0wvM7AjBZHcTiOmpNOXmjLGzdsZ_qNiENJgC2cigFDMKhcS_-mUTxZ01FAZ9tP-1QBtka8E_y84Arv_BobxO2qVYbiXyat6rmA3fDeYVFccWKkGRNC8JeY7A56ga5ElswYchqWi3aZRBlJmBYwog-i7lFQ9YN--GlSQ4eRRQsMgIODQoYjYmjH6P0icQcHmPnXE1jqaJKIgM8zpfEffm6eQWvHFxyXcRTfyW1ZWKVr85RVbaRRF4H8cnZKfDFEegzyR0qV7xy1q2GZLEwx_1SpTunXZ3c5cmULoGcIQponX3u5tJzKHfjFJUWz1savZjI579UqS-KDHvnv0mDPJU1IcIRzw8ALvA0qO4Jn2aXq1ni3CUhmY0ayEto_XGSEGUE-MRGq64gSkDqmNK4mnqFlq2BNX-3uS9YDjy2-hEx7iPp04Sz-FH9InRPgQeOANmxygQE-HLINybIGVnejEfD0ftd6j6F4J7UuUfM4KSD9GDAFlAou5zY3KmgwGRWxIuKSlOh--SoHuBqR_VQGTN7O7nlTkO7mpZuB1dTETQQR5nYOc640FcLBXSaNO4tt-PUvG-GUPKQV0sTGb8XHned1oMaz5jO2P8-Y0YmO_BIGKpmmYpOygokkT5jGbLF6JYxcRIlMG4JKfSOPn3CLM"
serverUrl = "dlgaas.beta.mix.nuance.com:443"
textInput = "test"

channel = create_channel(token, serverUrl)
stub = ChannelConnectorServiceStub(channel)
selector_dict = {
            "channel": "smartspeakerva",
            "language": "en-US",
            "library": "default"
}
# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('index.html') # render a template

@app.route('/startchat', methods=['GET'])
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
    return jsonify(message=''.join(message_array))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)