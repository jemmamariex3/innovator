# import the Flask class from the flask module
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('../google/api')
print(sys.path)
from dialog_innovate.innovate import *
import mimetypes

mimetypes.add_type('text/javascript', '.js')

# create the application object
app = Flask(__name__)
CORS(app)    #CORS origin issue still persists.. Hmmm.


# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C599/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3Njc5NTk2OSwiZXh0Ijp7fSwiaWF0IjoxNTc2NzkyMzY5LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiY2IyYTdiOTktZTkwZC00M2I2LWI4MDgtMzBmNmEyYzQ5ZmRmIiwibmJmIjoxNTc2NzkyMzY5LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.NzBnl8RPAfbk-3Og7qfr49yF2aKNw0Y23xtjRPDMrnKBBy--xN9Oz3KbTpm1vWPYWMTuOmK0ORe7-dbNO7GOuL8f1TuP9toOwxZ2XBRWT2xUIu3HAuIc9IovM6SPqpeY92H5QQ_EC6zosRls-8LFEavsh3kBhtteS7akVyvSy94RbPobDs-rhaXoE1BYbM-GKvyBy3KgW-23EMDv3urQAUd3tARFRxeFd-W3m76UCC_EEE3z08aN9Y82BN5A328DaNml8R1FCLjG1zXVqDMdNARJzInIqfs3VS70JFFC4b7CcukMPn-wFN0i50lFv1AeIkqhQ7OiCcK0AA7t0J-nRlWXSUNRmEKQ8_tJgmBoUXspWw33VCqe2lQFQalR91ZxT80vZIsbic20JRJlX-_DVzec4yt-DrDNsTL_QYq80_lWDbnoZYaCs-CZ85NxXUIl3nQo3a7tt0bpHKWtbJVh7__MyplMEuNl5CeIdDymXOpsToQHjzfh_yVdMcgMIFKmp1xvBh02KbxUZy7lqCxbYWKF4qwzEME5pGF9fx3bxDHzOlmEqdW4Z2wczi-3dl7QR8jH_LrO9Mr1_1xbcla-tPfIzTsTBhwkoE22UGuyITonfzdGDEvnogC59rBzf7uQCh6TTlJ0WVzjN2XVndtO1u6ruAXK_8DQ4hgP8RGfY-Y"
serverUrl = "dlgaas.beta.mix.nuance.com:443"
#textInput = "test"  Use this if you want to hardcode messages.

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
    print("Started the request. This is the session id: ", session_id)
    print("This is the start response: ", response)
    response, call = initial_request(stub, 
                            session_id=session_id, 
                            selector_dict=selector_dict
                        )                        
    va_response = response["payload"]
    message_array = []
    for prompts in va_response["action"]:
        for message in prompts["prompt"]["visual"]:
            message_array.append(message["text"])
    print("This should be the first automated sentence from the VA: ", message_array)
    print("We are returning this in JSON format for our front-end's GET request: ", jsonify(userText=''.join(message_array)))
    return jsonify(userText=''.join(message_array))

def continue_chat(): 
    global session_id

    if not request.json:
        abort(400)
    payload_dict = {
            "input": request.json   #This holds the message the user typed in the chat window.
    }
    print("The user sent a message to the VA. This should be the same session id as the initial request: ", session_id) 
    print("This should hold the user's message: ", payload_dict)

    response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=None
                                )
    
    va_response = response
    print("VA_Response: ", va_response)
    print("VA_Response in JSON for our front-end: ", jsonify(userText=va_response))
    assert call.code() == StatusCode.OK
    return jsonify(userText=va_response)

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