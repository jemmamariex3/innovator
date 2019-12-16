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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjQ3MDY0NSwiZXh0Ijp7fSwiaWF0IjoxNTc2NDY3MDQ1LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiNGZiMWViOGEtMmFlMi00OTEwLTg2ZmYtN2M5ZjlhNDA3MTliIiwibmJmIjoxNTc2NDY3MDQ1LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.VYk_s_dyRU3ECfW12cV7KdUk90h30jQAiOBznt8psRAirlnynAkj3yI0o3Sl0JVqUM_-rs02GxkC-0fHZrzd9nqnZ9PcBwiDa010C1BCs3J1tVE1zbcBZyHAu2zkWYNZoeZ5j87dWnPdq9GDMR3y3Li2N4oW25gIj802qEvuczaK_uWKH2J0z7IYkBO4pk9ZsmwfyWPRQlaJjl7z_UhDLCCeLV0MMUGc5MJU_C6QN-RpVBTa8uPqcXYh7Ueuoo_3o5Q6hMs-ukNho4Sg4840IDJMQFlOiB99Tj6essD2TV352bc0AFRzwGkt4AZjiTmsAspwulerrabCfjkqAkCY9OH_SJJLdzF9mU4JHWtyXiV-qq8oguGoC8H6yqT_KbX1zuvWTa10-nBucwufCpsjBZzAjjTzQVTjhHWBkIG0sdp5Zafmo5MqtCHJD796JB2Ire8U6I4PhCrfJ2HfVZ9gtniyTDDlHACD1bQ13fTmPL5-vwiLpoan2sdoeo0u6w798vuHE67jjzGyS6gog_5gZJGhDQWspPw-9q4UZkEg3MYvdWfuOLmh7VE00V9K7dF6TrPOTNfu5y2mQxOvSsXKH7cS0Z42UpxLKVN78EYLr6u5m3S7-ulku7c7EOMI8e3LvY5U0udIjRTiH1cxy4mbvXOcF809hztpLQOWWs-lVaI"
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