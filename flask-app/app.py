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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjgwMzkxNCwiZXh0Ijp7fSwiaWF0IjoxNTc2ODAwMzE0LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiYjgxMjk2MTktODlmZi00ZDA1LWI5NmMtMDQ1YmEzOTYwZGY0IiwibmJmIjoxNTc2ODAwMzE0LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.FQqYj1LGdzRSKzq9HjSvHXZon3U1OaEuw5JDs-UikUDP8nLFUQi22AR-w3Rs332-owShgNF71Z6i7PXzLXtI0SDGbBltMMBQjH_UE1YB6pxF3xUu4RSglnacN2h6c3sZzJdXhFDGfw5mRjjNSOzjGwmjTvpo20_S-bTruHpgzqQdZJPzPn-NjlzSlRr3onuUl3GSkotKJqYw1FcTzs9fzK6UtX7Fi5R8BnU5QVI_puOoSF-fw9o3EGTx7JWCmKc_Lxp6O_0XqpILR-dbQQkckk18SxJDYAn7b6G5zOfs5As-9wP0N4_6hGibrZZT5oj8e6-WZN59OE_Fmi77ZMtY1DepDE8M7jEVtzrfC2sjiMo_V3_c-9aHl2ni-Cpj7gT-8ZTKS3gTTQ4a_TPBeb-L3Djspw4ZwQAODoyzU4gBu6oKCefwaoxRyvwHd64sJc8sKYyvVjxfSmLeGLcsfbDPaJrB6NKRF5fAtr-v2Wyx1_ckqHxsFvNMzZYqDLBY9XxtBQTsKv5c69Mn47vqyID7LI65xV5htby9cUKdjGFh0cLM-r7giSU_DKEI6jrpPEU_06wgRlKGHkAyO4YSpwgfXTgxAhMgB3yQGB1MZEbNstaF3KGElzy5LMeIJ-xCKfyG0SAoaC4UI4idWlAPbOuMOO1Mat4zyC2fKtIlJfKEico"
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
    data_response = handle_response(response) #If the response requires a variable from us, we'll handle it here.
    if data_response is not None:
        print("This is the data_response: ", data_response)
        response, call = execute_request(stub,                  #Then we send it back to the VA,
                        session_id=session_id, 
                        # selector_dict=selector_dict,
                        payload_dict=payload_dict,
                        data_action=data_response
                    )
        print("Passed the data_action execute_request.")    
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