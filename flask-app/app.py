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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjQ3NDUyOSwiZXh0Ijp7fSwiaWF0IjoxNTc2NDcwOTI5LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiOTQ0ZGZiNGYtNjFiOS00N2Y0LTk0OTctMGU0ZGY4ZWU3ZmRlIiwibmJmIjoxNTc2NDcwOTI5LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.e4gcC9583wLFPr88Fqwj10o_c4WqFu6jkJZHbeF0Dv8ePV6Gqez5W-GxnM1T5ab4mS9VaioBStb6HuHvm2MlEho0GQ6ar5N4eunWjqIQKfTXVANFE6yz0I7wpWZdu3rZBpGvKbHWUuW8lmdzzQ7cahLKHx_S2CC-AWY3Q0WQ4CYB5mifqS_99onihFJC52LsbvNOqQ9FqPGUGjNvlRlGrzwOa5mNYIRqwAUch9e92LEE7yK1yyEy09fcz4Cq7iHE2ACwp9aABW0CUJmxd1ZLHTQVxhMLGjrCPGyNkdT8kMM-1tp3yFbEAzUX0zfEza1tuy9OBVrr199Xc0JCQjMIO6O193LD5WJ0_uvyFVLWan7qxGb002Vn1CXJj8-aKmJ93DcilKRkLErLFSAF-CDuJrOhW9CclKSuTb7eUZth-CC4x5yeQF9VFt_qFAir-qh7HuFvKOYzfeC1Yp4Fv4kvh8a1HRXvzx7te3Y81JgRKJU9DgzVC0mlTFizDdazNFRtLV3HlgK0od7_8rFKoKO2rR_qVXeiqaeJ1YGha4gGebUqxQKsfJTXeJij0p51Mp_0KUMJO4vMNeLrAgqY8QWjvqtVoarshC0PpbaUrb0KIGHbwLu4KIvSOqvkqZQ9Pz1qvHmAwRPuBkbouEiQ4wG89Is3y_R2APg6IfnfICwXz48"
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