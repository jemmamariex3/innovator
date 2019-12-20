# import the Flask class from the flask module
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('../google/api')
print(sys.path)
from dialog_innovate.my_backup import *
import mimetypes
from googletrans import Translator

translator = Translator()
initialLanguage = 'en'
mimetypes.add_type('text/javascript', '.js')

# create the application object
app = Flask(__name__)
CORS(app)    #CORS origin issue still persists.. Hmmm.


# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C617/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjgzMTE0MSwiZXh0Ijp7fSwiaWF0IjoxNTc2ODI3NTQxLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiODMxYjc5MzktNDJjYi00NmFkLWI3ZTQtYzVmYjAzZGZiOWE2IiwibmJmIjoxNTc2ODI3NTQxLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.pjfEIWxJcz-akgap9hNQ1OX9wmw5N98YeCYHLy6s-RJzMpCWby2gl7XzVDuXJJTESa2O-egkkVHGoK8Z9cCI9ZZXtz3nU42yBkqwbDHVyuLFZNXtWI7KAcJq3MooCG3bEybmcet0Rhe750RGgBmCAtk47oAdSNo6MwEwpSE3Q7Ht0NRHpIaYKon8Oiu5HdUkgReOhTAVdcAS59HxhD5XYV9y8SYoCfwwlLyqm-cd5ipzWjGZzYdG36Pijrd-2Ay6I0BqHbGqzyfvWUaZMLJtKGX97D7bLESow8oLkFEpu8uurFGzo4hilgsqKnvkEdWu-Y8u4Yq585lsvv1FGHmg-J6kDMZGWvHzeAJnHNOxEqsSdPNdq_gU0Ax8Ifn3-BU8oNZxlz9AodkPJVpfPx0_edUDqmuyq52f-KAc_345YD6g0KLNJO78IrbZYfFBNiJZCzNjSPCX0L6fg8I7xVjeJxUhE7jJcaOcASMsRz_h_YGOogOUYCXlwzmCQlCHMBFoGyhVzjWr8YqohqYtH0Ucwwdn9w7s3TbCk16Ep3BEdOMotE_ORz72bTLkgeBuZ6GgmF1qCXZnicvp8mX_ZZLvkIZ1K5m22zUfYtSyaxKmxh3P2Jeq0BIjC4dmwwcrHQQD4eFb4XbgvOE6Y72bftIb75KfCnX5LELoySgG7v3-WMA"
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
    global initialLanguage

    if not request.json:
        abort(400)
    payload_dict = {"input": {}}
    payload_dict['input'].update(request.json)
    userMessage = payload_dict['input']['userText']
    userLanguage = translator.detect(userMessage)
    print("this is after detecting: ", userLanguage)
    if userLanguage.lang is not "en":
        userMessage = translator.translate(userMessage)
        print("This is the message translated to english: ", userMessage)
        initialLanguage = userLanguage.lang
    payload_dict['input']['userText'] = userMessage.text
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
                if initialLanguage is not 'en':
                    print("This is the initialLanguage: ", initialLanguage)
                    newMessage = translator.translate(message["text"], dest=initialLanguage)
                    encodedMessage = newMessage.text.encode('utf-8').decode('utf-8')
                    message["text"] = encodedMessage
                message_array.append(message["text"])
    return jsonify(userText=' '.join(message_array))

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

@app.route('/tickets', methods=['GET'])
def tickets(): 
        if request.method == 'GET': 
            return jsonify(get_tickets_arr())

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)