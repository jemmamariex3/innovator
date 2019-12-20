import argparse
import sys
import logging
import json
import inspect
from functools import wraps

import uuid

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct

from grpc import StatusCode

from nuance.dialog.v1beta1.service_interface_messages_pb2 import *
from nuance.dialog.v1beta1.runtime_interface_messages_pb2 import *
from nuance.dialog.v1beta1.service_interface_pb2 import *
from nuance.dialog.v1beta1.service_interface_pb2_grpc import *

log = logging.getLogger(__name__)

global data_class 

"""

Generic Code

"""

# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C599/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjgxMTU4MywiZXh0Ijp7fSwiaWF0IjoxNTc2ODA3OTgzLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiOThlZmQwMGItYzQyMS00N2IwLTlhNDYtMjA1Y2FmNDgzYmMyIiwibmJmIjoxNTc2ODA3OTgzLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.ed-ToNzxlpy3KY6s7-Hw-INYrE7j_6joTSDKiwRbt2X5ftucotnKBl9-1Mz4MdzeeCK9QnZf3TMFORc4KCXDru_fP5BmAXG8EYu4BRvZgReNSmaIoZV8wFUZ7RLmLmEUZDCF3QzpGpP5K_jlohJPtqB0jyeKLYbOsDT-UnF5yUWFqHFIiMB7a8GXbdock-jn0oS51jYMyjHAI_5rkF4I95N_esej1T9bdmRKoaMkrgtxLJ5av3y-vNU0kqyjS3bMsLp3tVBrqfZt3vuegxeTks12YVPh_aan-dhpLt3qARIOt3pxpqma3fNYeFJaeJ7Q64xYh4fW7NnZlqNXIXMe4656g6SogiDJEYoWVV8cpnUqqvU-i3RSM7ctbT70Ko14sJjZMHBpnOkpJ0vk0ubzjqNVVB4lPGICWyVhZde3VQFxhdIEG4YECV1Zh3cWGkVx29l9BvvH5oxpnV0CcWj8H-R17wUEnggF2gG83gB-0IZF313Zhbs8b0X-slhlceTiGfkdkgUNsUE89qG2RGEH58KvfLqyuNnmj9kt-IECnGt80vcIVBGSSqYu9XdZOIONIW73EQlNMOCloVXfNQ-CV64Y0wJpaDFGOC8MyZ4ySSQ1qyC4NzxQjCnW0HtYItjJxDzVMVYS58HfK4-WzFI1OCd1DT_I2rgiO3Cr3Jfn_7I"
serverUrl = "dlgaas.beta.mix.nuance.com:443"

selector_dict = {
            "channel": "web",
            "language": "en-US",
            "library": "default"
}
#textInput = "test"  Use this if you want to hardcode messages.



def create_channel(token, serverUrl):
    
    log.debug("Adding CallCredentials with token: ", token)
    call_credentials = grpc.access_token_call_credentials(token)
    channel_credentials = grpc.ssl_channel_credentials()
    channel_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
    channel = grpc.secure_channel(serverUrl, credentials=channel_credentials)
    return channel

def read_session_id_from_response(response_obj):
    try:
        session_id = response_obj.get('payload').get('sessionId', None)
    except Exception as e:
        raise Exception("Invalid JSON Object or response object")
    if session_id:
        return session_id
    else:
        raise Exception("Session ID is not present or some error occurred")


def start_request(stub, model_ref, session_id, selector_dict={}):
    selector = Selector(channel=selector_dict.get('channel'), 
                        library=selector_dict.get('library'),
                        language=selector_dict.get('language'))
    start_payload = StartRequestPayload(model_ref=model_ref)
    start_req = StartRequest(session_id=session_id, 
                        selector=selector, 
                        payload=start_payload)
    print("This is the start_req: ", start_req)
    start_response, call = stub.Start.with_call(start_req)
    response = MessageToDict(start_response)
    print("This is the start response: ", response)
    return response, call

def execute_request(stub, session_id, selector_dict={}, payload_dict={}, data_action=None):
    selector = Selector(channel=selector_dict.get('channel'),
                        library=selector_dict.get('library'),
                        language=selector_dict.get('language'))
    execute_input = None
    execute_data = None
    if not data_action:
        execute_input = Input(user_text=payload_dict.get('input').get('userText'))
        print("This was not a data action. This is the input we are sending: ", execute_input)
    else:
        v = Struct()
        v.update(data_action.get('value'))
        execute_data = RequestData(id=data_action.get('id'), value=v)
        print("This is the Request Data Object: ", execute_data)
    # session_data = SessionData()
    execute_event = Event()
    execute_payload = ExecuteRequestPayload(
                        input=execute_input, 
                        event=execute_event, 
                        session_data=None, # DEFUNCT
                        data=execute_data)
    print("This is the execute_payload: ", execute_payload)
    execute_request = ExecuteRequest(session_id=session_id, 
                        selector=selector, 
                        payload=execute_payload)
    print("This is execute_request: ", execute_request)
    execute_response, call = stub.Execute.with_call(execute_request)
    response = MessageToDict(execute_response)
    print("This is the response after Execute stub call: ", response)
    return response, call

def stop_request(stub, session_id=None):
    stop_req = StopRequest(session_id=session_id)
    stop_response, call = stub.Stop.with_call(stop_req)
    response = MessageToDict(stop_response)
    return response, call

def data_access_node(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        success = True
        value = {}
        try:
            ret = func(*args, **kwargs)
            value.update(ret)
        except Exception as ex:
            logging.exception(ex)
            success = False
        value.update({
            "returnCode": "0" if success else "1"
        })
        ret = {
            "id": inspect.stack()[0][3],
            "value": value,
        }
        print("This is in data_access_node function. This is what it returns: ", ret)
        print("This is the value for variable value: ", value)        
        return ret
    return func_wrapper

def process_data_request(data_action):
    global data_class
    print("This is the data_action in process_data_request: ", data_action)
    func = getattr(data_class, f"{data_action['id']}")
    if func:
        try:
            return func(data_action)
        except Exception as e:
            logging.exception(e)
    return None

def handle_response(response):
    data_action = None
    actions = response['payload']['action']
    # Loop through actions and print all visual prompts, 
    # then execute data action returning formatted response
    for action in actions:
        if "prompt" in action:
            va_prompt = ''.join([x['text'] for x in action['prompt']['visual']])
            print("This is all the text from the prompt visuals: ", va_prompt)
        elif "data" in action:
            data_action = action['data']
            print("Looks like this response was from a data access node: ", response)
            print("This is the data_action parsed from the response: ", data_action)
    if data_action is not None:
        print("Entering process_data_request with the data_action")
        return process_data_request(data_action)
    return None

def main():
    channel = create_channel(token, serverUrl)
    stub = ChannelConnectorServiceStub(channel)
    response, call = start_request(stub, 
                            model_ref=modelUrn, 
                            session_id=str(uuid.uuid1()), # Create a session id
                            selector_dict=selector_dict
    )
    print("In main(), just started the request. This is the response: ", response)
    session_id = read_session_id_from_response(response)
    print("This is the session id: ", session_id)
    inited = False
    data_action = None

    payload_dict = {"input": {}}
    response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=data_action
                            )
    print("This is the first automated reply: ", response)
    
    payload_dict['input'].update({
        "userText": "Show me the open tickets"
    })

    print("This is the payload that I will be sending for ticket status intent: ", payload_dict)
    response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=data_action
                            )    
    print("This is the response after sending in hardcoded message: ", response)
    data_action = handle_response(response)
    print("This is the data_action from handle_response(response): ", data_action)
    payload_dict = {}
    response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=data_action
                            )
    print("This should be the response after sending the VA the data_action string: ", response)        
    print("Cool, i'm going to end it now. I hope you do well man.")
    stop_request(stub, session_id)


"""

Custom Code

"""

class DataClass:

    """
    Each function is a DA node. Simply return the values.
    """

    @data_access_node
    def GetTicketByStatusData(self, data):
        entity = data['value']['_concept_TICKET_STATUS']
        return {
            "returnMessage": "yo what's up homie, it worked",
        }

data_class = DataClass()

if __name__ == '__main__':
    main()
