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
#modelUrn = "urn:nuance:mix/eng-USA/A174_C654/mix.dialog" Broken.
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3Njg2MzU2MCwiZXh0Ijp7fSwiaWF0IjoxNTc2ODU5OTYwLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiYTI5MTczOGUtNTg1NC00ZmQyLWJhYWMtZGVmODAxMzEzODkxIiwibmJmIjoxNTc2ODU5OTYwLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.CY_FlsD2yW-KR7PCMUxRupADN5IK3ug5QHe1wsn3yva8Mk2JlzlEDmEkSSc4z4heJQAZmV1NFI-bLvxDnqzYfH3KnjPUhkCPP_Yl9xpmHHl50AXshGtr1gAccCsdmqoqihtkEfckcoYLikAPZWP5C10VJ7FVSTfOZYxt0CUsbaPexsat-g5B491ArldO7fbqf6iM9dy9vdkA5mo1Ovulllm_HWcyeHW1ATGqLrYD1shBEOlkB-Z1MQHREWt4whT5udAn5wjY26PoR8IQtBfxavd6992aT2Q67J9uPt_Dze3h77oMJX2U2LW_VVpo_wSqzWUjJuDVZHXEo2R6GLw8W9zvd8WKWSFnJfs9J58MTJdHE-i81fkxiUUCc5f4axqOYBV3dmZyMlA43aub5CW37taX7g0AmhuudVqR1Ewq9MKaFX8_liUYBvloRjXoO5eivTh5kry9RnKd1-_nMu47bQMZlSnOTGcWx03l-DXLT0THlKqROdTTKZyWad_i8S1qhU2Lfn-ggyDP7u5MPXkIXVGrXfjaWFKxu2ZUoO0s31_3BEKzxCA3BXbPoZ1Yu0JdIk0DOrikxPxTEot397xV6Nnop51K5l9ezQ9khofPAMq0Q3ZXTSnShrOCJZKjUqUrvw_JOK9snKcYxZ49Pa0mIGmtJcvs_JAagDVoJve9c-Y"
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
    print("This is the userLangage that it detected.. ", userLanguage.lang)
    if(userLanguage.lang is 'en'):
        print("This should be caught here.")
    if('en' in userLanguage.lang):
        print("what the heck is this")
    if(userLanguage.lang is initialLanguage):
        print("this should also be caught?:",userLanguage.lang)
    assert call.code() == StatusCode.OK
    va_response = response["payload"]
    message_array = []
    english_check = False
    for item in va_response["action"]:
        if 'prompt' in item:
            for message in item["prompt"]["visual"]:
                if 'en' in initialLanguage and len(initialLanguage) <= 3:
                    english_check = True
                if english_check is False:
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