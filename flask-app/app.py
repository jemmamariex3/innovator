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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3Njc4MzYyOSwiZXh0Ijp7fSwiaWF0IjoxNTc2NzgwMDI5LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiMmMzN2MwNTAtMTNjZC00ODYwLTg0ODUtYTBiZDMzMmQ3ZTUyIiwibmJmIjoxNTc2NzgwMDI5LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.DVGhpnNBWUajFymN4JxfvjYq1caZP3d6Qon2ICFMeYlS9POSL6cBIuipNQlAEZy_xn6ERoJS3Slydq8cyCzXjvos8MtS_Ao6TkjDb9dsmgIUBSm-F1CdlgUOAWd4sW0VEiUlYxT311RABzoRWP1yColiH13E9sPJrhd9dNkxnPH8ixrFyUD8uzuXH7yc-_SlrcozPFuPfKi7K43bJzdYGnEHfDCwco4p2TrvxqVMHjzTo-MCpTSVB_eiIIv_KQGi3kY0OQfUbmc7UivprVspYGNdOo81WEBnRIj43ThOFuBiw9Y-vZdKWRqUrqut9rjd7Jb9LDvtNyqgFMWQ67mEXQiFUR_k88mUFGSmhujwVyIYbXbZXOoiTUFXoQiBS70CK5UCVxb9Mx3gKLZlf1INC9h7IheCGhwUuN9EbwuHTvrNp8Qxek19Te3C2DxMlypO_KNAlLl2M8cATWSzCo-CpZ52fGWOr253WI1yRYBOT14ge4KXcguwtCGuhqpfheZ_qaUbYWPwoOJWQ9-zpn-T_QpuQBTSg9o9zMtxaKm1mTWvKn0iCI333e3oQm3cEb2JQ4kHjA1RyKlupu20Dv5-D4yGgZeXAOxSqsssh4ZyxBZ172fLNCbS6294SyUaNHw9vm6AmsNy_Hy2eLTwAxJo4HZ8AQIIzPVVSnHKc8FRMcs"
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
                                    data_action=data_action
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