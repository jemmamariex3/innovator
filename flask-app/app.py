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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3Njg0MTAzMSwiZXh0Ijp7fSwiaWF0IjoxNTc2ODM3NDMxLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiZDhkZWYwNjAtOTM3My00YjhjLWIzNGItYTEzYzE4ZWQwZDYxIiwibmJmIjoxNTc2ODM3NDMxLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.RgNGeS4wBpctQY0OF5g2-Ys4lyLDFaMpj6ZjDaPiT4am66MyLjWhKFqTe5urXY64D4yRNGdVWoiiRk9_Rz-LcRClCRIskGn6P3mwFPdqHlkoUqq-9H27IjDuixIAFHoY4_SNBBtL5MxqmNes0RwbAcVDN8CpSmE8T8L5BGCHgSmLxwqynX35vPvdl4dhHWOjKPrK_OlJwrdKY-WPgIZffnwE-7WhXaone_lQyTnk25j2objB_cZ97m59G5zlNOlf0SaST2i2vkjKJ2w5t7ua0RM558QHBSOhvZpIBlH7cCVyB1qryVkKZEzkoyWBAKGi6Rga9ldEDmkmVaiYMgJFQ77ZY3RXOjTEpwVs0Guj5YRakZOZCpufVVfFS3fJxp1zRqNfnlPQLc1SBVj68x6q5wKYseHp2Lxb-diZbLPkY9xkQqrnJJaJ5eOFyCt0TSp2CJWNd4oQwBIgutqYX5quv8NUifQKRd9htYmN64Da39PgUNELdYrh-KKFVG-wvFpTKfa7d3b6GQK5ygDmi4dI0bmyM6ihBzpAg4VRVz-QbWUpKmaDDs4NWmeYsYEUnlJwOsa_iEl4YnHQ8-v_f76COOHaxHXJ5UQ6xHHkO5O8KEp4FwLhFuOc5RMuzJ_fizEWjIu_UTXWrL5aM4x2yOg-u1LsoEdXISWdAp61fybIKLc"
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