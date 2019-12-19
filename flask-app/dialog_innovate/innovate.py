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
modelUrn = "urn:nuance:mix/eng-USA/A174_C599/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3Njc0MTE4MiwiZXh0Ijp7fSwiaWF0IjoxNTc2NzM3NTgyLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiNjVlNjg5MDctYTViOC00MDMzLWI1MDItYWUyODI4N2RiZjYwIiwibmJmIjoxNTc2NzM3NTgyLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.ZaI-Z9jF5qkwpqu8-QOVcm4oW-U1gmCMaC2pMAYHTn9uIqA5ws_iB0y5FZ-h01qIlkwE9CnACgmua6KPRBSDjaoY-kjfUh0oPNgr0x1sBuGWkpL512Pl1h_-nyHub5ZlXf7nILhbzhY-RmxIJ61FVi1jPSp8eZwOixEDCbbqw78o5LiFvOqKa7EZ318oK-5dmt0yxWiREOHCqc4bCAjlrIO06cv6r8Xfq6g9bIpoKtyLk5mOtC5BHotxBHQwZDDDOVOtXT4pHaD6jQrYeAeI3jCaTtpU3QXi1HWqV2GQTiDgduB1RiUrijQwd2aj0U0AXJFm-XG3KTdbAkxO4JcATIho1rRDe-xahnpsfW-85oDEkvKuWjzvegon31YtrUwMO3hUFEKsTQomNma5Q0lkPVbx0BRkPqZeaVuPk21tGtT4IHEC_eNEk3l9W3Y_5kbU-nd3P3Nc6iF-4duOZReMHSEbVAafU8XEqAAQRuIekP2WjympkuxAgNeuFt1-XX2Czo1h8fsEY1ZQ_1An-VTI6mGIst4_sVLzcZDVWf97hYnYCA1r0Zs9fCViaLtzQVkdNzRhYzJCYec2Gfb0v8-RZa3BW8hsEGPVVsCaaIvTwVgVkyXYRI1Xbv1T7sQKiin3V7fqDHRDbxHI2QQCPaQVJcCDo2bHI4yk9zammWbpSok"
serverUrl = "dlgaas.beta.mix.nuance.com:443"
textInput = "test"

Leaving it here in case we want to hardcode test. But in the end, we'll using this api info in app.py
"""

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
    start_response, call = stub.Start.with_call(start_req)
    response = MessageToDict(start_response)
    return response, call

def initial_request(stub, session_id, selector_dict={}, data_action=None):
    selector = Selector(channel=selector_dict.get('channel'),
                        library=selector_dict.get('library'),
                        language=selector_dict.get('language'))
    initial_input = None
    initial_data = None
    initial_event = Event()
    execute_payload = ExecuteRequestPayload(
                        input=initial_input, 
                        event=initial_event, 
                        session_data=None, # DEFUNCT
                        data=initial_data)
    execute_request = ExecuteRequest(session_id=session_id, 
                        selector=selector, 
                        payload=execute_payload)
    execute_response, call = stub.Execute.with_call(execute_request)
    response = MessageToDict(execute_response)
    return response, call   


def execute_request(stub, session_id, selector_dict={}, payload_dict={}, data_action=None):
    selector = Selector(channel=selector_dict.get('channel'),
                        library=selector_dict.get('library'),
                        language=selector_dict.get('language'))
    execute_input = None
    execute_data = None
    if not data_action:
        execute_input = Input(user_text=payload_dict.get('input').get('userText'))
    else:
        v = Struct()
        v.update(data_action.get('value'))
        execute_data = RequestData(id=data_action.get('id'), value=v)
    # session_data = SessionData()
    execute_event = Event()
    execute_payload = ExecuteRequestPayload(
                        input=execute_input, 
                        event=execute_event, 
                        session_data=None, # DEFUNCT
                        data=execute_data)
    execute_request = ExecuteRequest(session_id=session_id, 
                        selector=selector, 
                        payload=execute_payload)
    execute_response, call = stub.Execute.with_call(execute_request)
    response = MessageToDict(execute_response)
    print("This is the VA's response from our ExecuteRequest call. If it's a DA node, we'll do another execute request: ", response)
    data_action = handle_response(response) #If the response requires a variable from us, we'll handle it here.
    if data_action is not None:
        print("This is the data_action: ", data_action)
        response, call = execute_request(stub,                  #Then we send it back to the VA,
                        session_id=session_id, 
                        selector_dict=selector_dict,
                        payload_dict=payload_dict,
                        data_action=data_action
                    )
        print("Passed the data_action execute_request.")
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
        logging.debug(f'-> {ret}')
        return ret
    return func_wrapper

def process_data_request(data_action):
    global data_class
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
            print("This is the VA_Prompt: ", va_prompt)
        elif "data" in action:
            data_action = action['data']
    if data_action is not None:
        return process_data_request(data_action)
    return None

def main():
    log_level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s %(levelname)-5s: %(message)s', level=log_level)
    channel = create_channel(token, serverUrl)
    stub = ChannelConnectorServiceStub(channel)
    selector_dict = {
            "channel": "web",
            "language": "en-US",
            "library": "default"
        }
    response, call = start_request(stub, 
                            model_ref=modelUrn, 
                            session_id=str(uuid.uuid1()), # Create a session id
                            selector_dict=selector_dict
                        )
    session_id = read_session_id_from_response(response)
    print("This is the va start response: ", response)
    payload_dict = { #Hardcoded first message
            "input": {
                "userText": "Start"
            }
        }
    data_action = None
    response, call = execute_request(stub,                  #This response should be the intro node.
                        session_id=session_id, 
                        selector_dict=selector_dict,
                        payload_dict=payload_dict,
                        data_action=data_action
                    )    
    print("intro messages: ", response)
    #response, call = stop_request(stub, session_id=session_id)
    #assert call.code() == StatusCode.OK
    #print("This is all the messages", message_array) # Request just started. Response should have first auto-message.   
    
    log.debug(f'Session: {session_id}')
    print(f'Session: {session_id}\n')
    assert call.code() == StatusCode.OK
    inited = False
    data_action = None
    payload_dict = { #Hardcoded first message
            "input": {
                "userText": "Show me the open tickets"
            }
        }
    response, call = execute_request(stub,                  #This response should be requesting for a return message / data_action
                        session_id=session_id, 
                        selector_dict=selector_dict,
                        payload_dict=payload_dict,
                        data_action=data_action
                    )
    print("This should be asking for returnMsg: ", response)
    data_action = handle_response(response)         # This helper function should handle the data_action formatting.
    print("This is the data_action", data_action)
    response, call = execute_request(stub,                  #Then we send it back to the VA,
                        session_id=session_id, 
                        selector_dict=selector_dict,
                        payload_dict=payload_dict,
                        data_action=data_action
                    )    
    print("This is the VA's response to Data Action: ", response)
    print("Going to end it now!")
    response, call = stop_request(stub, 
                        session_id=session_id
                    )    
"""

Custom Code

"""

class DataClass:

    """
    Each function is a DA node. Simply return the values.
    """

    @data_access_node
    def GetTicketByStatusData(self, data):
        entity = data['value']['_concept_TICKET_STATUS'] #Toss in ticket-logic functions in here.
        return {
            "returnMessage": "yo what's up homie, it worked",
        }

data_class = DataClass()

if __name__ == '__main__':
    main()
