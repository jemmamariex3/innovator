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
modelUrn = "urn:nuance:mix/eng-USA/A174_C527/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjQ4MjY2NiwiZXh0Ijp7fSwiaWF0IjoxNTc2NDc5MDY2LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiMmRlMzZiN2QtNWU5Yy00MzkwLWFmNTAtNWI3Y2NlZGFjNDJkIiwibmJmIjoxNTc2NDc5MDY2LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.CeaSiCFfAWhCm7K3PA1tzy-tT-Jrl7idw1Dh43SSssLcbfxVd0oWE1I_ZyeBWUQ8AXDNMmPGAaL4xzdPfNLhAiB9JXYgO43dF27loTVbSHTgxcE8ED5d54DwFJx3FLaZpRczBiQ1RMLGFDR8IiRE2M4vj84X79jL4ZuypCm6DGLS1Vvm8kjczidujazIKgd8REIgnG4UiPIWXKQ85yuV9kmCoRdjZHaL1UUFxfBKozxZIyA0I6xUPgp1E8rleabdwO2UwgVzmGyzR67uP-fXwWbZcT7a7sDKNn02zO89PtwrB6228zcTvDlBFDUzYYxfK2GlBqnsFN2rjoFWKLpD4hJKt6L_1oghKKu_PhFNZovsu5gd9op_gvGjgrh8GfOHPtjALWTMoaOHn6Sc6nKGHrpNolhxtRr0tyVcyKdp0G1DrrnpKCe2wvzOqo62HyuS2Lpy-jTr3maxZSEZR9Ifm1bD8OGmA4GYqApp6MMZolDM98001UeYj70tXqp-Rldol-gNaiHQR_3iY89l15AOMrnOKUn9trdrlACUENlxkprIIMM69t2qTDfChhEuLGGnDB5NgIGjJMeuRvEARwHG5H6HKXBwC5pzzWjxYNLcooy1jTkIz_sHIcJm3KmwoyCMZmMkI7l8v3aGoVQ2oE-bPnv-LqqN9KHJi8Xykb6JpN8"
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
    for prompts in va_response["action"]:
        for message in prompts["prompt"]["visual"]:
            message_array.append(message["text"])
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