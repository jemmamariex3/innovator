# import the Flask class from the flask module
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('../google/api')
print(sys.path)
from dialog_innovate.my_backup import *
import mimetypes

mimetypes.add_type('text/javascript', '.js')

# create the application object
app = Flask(__name__)
CORS(app)    #CORS origin issue still persists.. Hmmm.


# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C599/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjgxNTMyMiwiZXh0Ijp7fSwiaWF0IjoxNTc2ODExNzIyLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiZjdmMWVlYmUtZDM1Yy00OTNmLWI2NWItOWI3YWY5NzE1MzA3IiwibmJmIjoxNTc2ODExNzIyLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.MjHssU2DuX0JQN9ceJKUtP8IMGBMqGH2pnNgl5x5aFEYNGT5-1Bn8I279GPYkPw_1cb8LZKPrsWIzven8PitOcod9reZ7zWbQghMvIDO_5-jeXudrNqTF5s9ykKxpAAw0zcWhm3MnVnVhZp5gmpMnJ-ycLzGgxTYXVW_H1utbqJsAYdR8Y09OoisLjr5rbYraaScXvfAy9zGy6yZs34VD_yA5bG6R3axh6ZZeyrrR-i9kWQQ7MH81QuiiWEFBwtKpZ1jUqX4QLrQ7S4NXZGk28rpqTixOhCPA6LMO59i65c1wUXrmDJmEzpT5NsINU22vmF1-UFBx_J4oFA3HxUGH3ZW39Np5YpvIGMbqH9YQ38_icLU3_04eMc5gNBRkKq1jqh1vH3mD2vXkJpdf9iVAhzJh_7jvqnM6XaTiUzyEQ_ztGbwRZzgXulFJUa9c5YiE7w_RX_WLkv-8VqyiV5MdsN9PNTdDO2RKYALufyxjvWlFN0VAZP6lg_xBdV0rSVg9oY0_fcNFeeJE-uR-v5b4lgXrbSSNYXaexZUQ34zQ9ABx0QiVJrbLCRdTKhSDrZclTQJzaLvCTkFVUNgZZ70wLBSsteqJJJrR-sVN3tZVMjG9Catj8t193DVudKd-yCECY1796OuT2RONKksIKMDlI87CZm-KYe9zQMWARkf7nI"
serverUrl = "dlgaas.beta.mix.nuance.com:443"
#textInput = "test"  Use this if you want to hardcode messages.

channel = create_channel(token, serverUrl)
stub = ChannelConnectorServiceStub(channel)
selector_dict = {
            "channel": "web",
            "language": "en-US",
            "library": "default"
}
session_id = ''
payload_dict = {"input": {}}
data_action = None

def start_chat():
    global session_id
    global payload_dict
    response, call = start_request(stub, 
                            model_ref=modelUrn, 
                            session_id=str(uuid.uuid1()), # Create a session id
                            selector_dict=selector_dict
                        )
    session_id = read_session_id_from_response(response)
    print("Started the request. This is the session id: ", session_id)
    print("This is the start response: ", response)
    inited = False
    data_action = None
    response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=data_action
                            )
    print("This is the first automated reply (unformatted): ", response)                        
    va_response = response["payload"]
    message_array = []
    for prompts in va_response["action"]:
        for message in prompts["prompt"]["visual"]:
            message_array.append(message["text"])
    print("This should be the first automated sentence from the VA (formatted): ", message_array)
    print("We are returning this in JSON format for our front-end's GET request: ", jsonify(userText=''.join(message_array)))
    return jsonify(userText=''.join(message_array))

def continue_chat(): 
    global session_id
    global payload_dict
    global data_action

    if not request.json:
        abort(400)
    payload_dict = {"input": {}}

    payload_dict['input'].update(request.json)
    print("The user sent a message to the VA. This should be the same session id as the initial request: ", session_id) 
    print("This should hold the user's message: ", payload_dict)
    response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=data_action
                                )
    print("VA_Response from initial message: ", response)
    data_action = handle_response(response)
    if data_action is not None:
        print("this response needs some additional data logic: ", response)
        payload_dict = {}
        response, call = execute_request(stub, 
                                        session_id=session_id, 
                                        selector_dict=selector_dict,
                                        payload_dict=payload_dict,
                                        data_action=data_action
                                )
    print("VA_Response in JSON for our front-end: ", response)
    assert call.code() == StatusCode.OK
    va_response = response["payload"]
    message_array = []
    for item in va_response["action"]:
        if 'prompt' in item:
            for message in item["prompt"]["visual"]:
                message_array.append(message["text"])
    print("This should be the first automated sentence from the VA (formatted): ", message_array)
    print("We are returning this in JSON format for our front-end's GET request: ", jsonify(userText=''.join(message_array)))
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