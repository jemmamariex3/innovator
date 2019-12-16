import argparse
import logging

import uuid

from google.protobuf.json_format import MessageToJson, MessageToDict

from grpc import StatusCode

from google.api.service_interface_messages_pb2 import *
from google.api.runtime_interface_messages_pb2 import *
from google.api.service_interface_pb2 import *
from google.api.service_interface_pb2_grpc import *

log = logging.getLogger(__name__)

def test():
    print('nice')

'''
def parse_args():
    parser = argparse.ArgumentParser(
        prog="dlg_client.py",
        usage="%(prog)s [-options]",
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=45, width=100)
    )

    options = parser.add_argument_group("options")
    options.add_argument("-h", "--help", action="help",
                         help="Show this help message and exit")
    options.add_argument("--token", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("-s", "--serverUrl", metavar="url", nargs="?",
                         help="Dialog server URL, default=localhost:8080", default='localhost:8080')
    options.add_argument('--modelUrn', nargs="?",
                         help="Dialog App URN, e.g. urn:nuance:mix/eng-USA/A2_C16/mix.dialog")
    options.add_argument("--textInput", metavar="file", nargs="?",
                         help="Text to preform interpretation on")

    return parser.parse_args()
'''

def create_channel(token, serverUrl):    
    log.debug("Adding CallCredentials with token %s" % token)
    call_credentials = grpc.access_token_call_credentials(token)

    log.debug("Creating secure gRPC channel")
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
    log.debug(f'Start Request: {start_req}')
    start_response, call = stub.Start.with_call(start_req)
    response = MessageToDict(start_response)
    log.debug(f'Start Request Response: {response}')
    return response, call

def execute_request(stub, session_id, selector_dict={}, payload_dict={}):
    selector = Selector(channel=selector_dict.get('channel'), 
                        library=selector_dict.get('library'),
                        language=selector_dict.get('language'))
    input = Input(user_text=payload_dict.get('input').get('userText'))
    event = Event()
    # session_data = SessionData()
    data = RequestData()
    execute_payload = ExecuteRequestPayload(
                        input=input, 
                        event=event, 
                        session_data=None, 
                        data=data)
    execute_request = ExecuteRequest(session_id=session_id, 
                        selector=selector, 
                        payload=execute_payload)
    log.debug(f'Execute Request: {execute_payload}')
    execute_response, call = stub.Execute.with_call(execute_request)
    response = MessageToDict(execute_response)
    log.debug(f'Execute Response: {response}')
    return response, call

def stop_request(stub, session_id=None):
    stop_req = StopRequest(session_id=session_id)
    log.debug(f'Stop Request: {stop_req}')
    stop_response, call = stub.Stop.with_call(stop_req)
    response = MessageToDict(stop_response)
    log.debug(f'Stop Response: {response}')
    return response, call

def main(): 
    #args = parse_args()
    log_level = logging.DEBUG
    logging.basicConfig(
        format='%(asctime)s %(levelname)-5s: %(message)s', level=log_level)

        
    session_id = read_session_id_from_response(response)
    log.debug(f'Session: {session_id}')
    assert call.code() == StatusCode.OK
    """
    payload_dict = {
            "input": {
                "userText": textInput
            }
    }"""

        


if __name__ == '__main__':
    main()

"""
 serverUrl = dlgaas.beta.mix.nuance.com:443
 token = import from ../token_scripts
 modelUrn = urn:nuance:mix/eng-USA/Innovate/mix.dialog


--token $TOKEN 

    modelUrn = "urn:nuance:mix/eng-USA/A174_C517/mix.dialog"
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjQ1NTM2NywiZXh0Ijp7fSwiaWF0IjoxNTc2NDUxNzY3LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiN2MxMzJkMmQtOGQwMS00MDU0LTkxM2QtN2ZlZTFhNmQxMDMwIiwibmJmIjoxNTc2NDUxNzY3LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.j4bRAQ_dPVb-yF3u21Xr8mQcdTVMjOfi7uq371iGInhrDBxJh4FrfFyU2_R2oQ7KZSdZiQEcsv-TN5m6cpOU2njQV6KT40dMSj94ZWv8A3Bkogra7jD8re7fUbBPFtupKuEZOhgJsS8_36a3P2YQU4oZhJAJWr1FAqmI6BSsjwkIDVoK9jaNFRiai32V7AzdnjyhYd7XWspuocdjUlb5Wpd69vUUc8tENjRKEwHRSenOl5atziXZoKsjOb0xa0Q08jg4TfmtnNYB4oPWSfwyoUw8_3-XdfasVtFW-mtL9IcBg-pVcsFCJJXjE8tsice3LBzkJlWbwmgV0JzKhBPA2vbINADBzM3cW4YbjXk-n0D7rYs-61-6LwB4rIR2YZpFFeDv3leIzKyYfzaPSfh0eurFnwD-xEZPyLrNzjfbOHa63WgkfjZs6GubLCDvTz2xXSQuEQX3U-ENSMAJKUhUVPPqZQGchOoo6FDJ9vRLL_-586qTo8SK-Tak4sf45kAcbOKC6IMWWM2D6_d4RfnyLiSqRpXQsXvGpWSguzKegaOjYLfviF2pkJKXyvKhbAugx3e6_E0phCNJdhWeLRNGLVNojl8gLkBx1iWI3CxSpC74b0KV9bzcFRtsBatBaJglxFz1kmnx_-Qbcqk6bLmPF1FLtFp9iAuVizwFvKNm3Xw"
    serverUrl = "dlgaas.beta.mix.nuance.com:443"
    textInput = "test"   

        response, call = execute_request(stub, 
                            session_id=session_id, 
                            selector_dict=selector_dict,
                            payload_dict=payload_dict
                        )
        assert call.code() == StatusCode.OK
        response, call = stop_request(stub, 
                            session_id=session_id
                        )
        assert call.code() == StatusCode.OK

"""
