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

def _wrap_with(code, bolden=False):
    def inner(text):
        c = code
        if bolden:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')

red_bold = _wrap_with('31', True)
green_bold = _wrap_with('32', True)
yellow_bold = _wrap_with('33', True)
blue_bold = _wrap_with('34', True)
magenta_bold = _wrap_with('35', True)
cyan_bold = _wrap_with('36', True)
white_bold = _wrap_with('37', True)

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
    options.add_argument("--nmaid", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("--token", nargs="?", help=argparse.SUPPRESS)
    options.add_argument("-s", "--serverUrl", metavar="url", nargs="?",
                         help="Dialog server URL, default=localhost:8080", default='localhost:8080')
    options.add_argument('--modelUrn', nargs="?",
                         help="Dialog App URN, e.g. urn:nuance:mix/eng-USA/A2_C16/mix.dialog")
    options.add_argument("--secure", action="store_true",
                         help="Connect to the server using a secure gRPC channel.")
    options.add_argument("--rootCerts", metavar="file", nargs="?",
                         help="Root certificates when using secure channel.")
    options.add_argument("--privateKey", metavar="file", nargs="?",
                         help="Certificate private key when using secure channel.")
    options.add_argument("--certChain", metavar="file", nargs="?",
                         help="Certificate chain when using secure channel.")
    options.add_argument("--debug", action="store_true",
                         help="Show debugging logs.")

    return parser.parse_args()

def create_channel(args):
    call_credentials = None
    channel = None

    if args.token:
        log.debug("Adding CallCredentials with token %s" % args.token)
        call_credentials = grpc.access_token_call_credentials(args.token)

    if args.secure:
        log.debug("Creating secure gRPC channel")
        root_certificates = None
        certificate_chain = None
        private_key = None
        if args.rootCerts:
            log.debug("Adding root certs")
            root_certificates = open(args.rootCerts, 'rb').read()
        if args.certChain:
            log.debug("Adding cert chain")
            certificate_chain = open(args.certChain, 'rb').read()
        if args.privateKey:
            log.debug("Adding private key")
            private_key = open(args.privateKey, 'rb').read()

        channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates, private_key=private_key,
                                                           certificate_chain=certificate_chain)
        if call_credentials is not None:
            channel_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        channel = grpc.secure_channel(args.serverUrl, credentials=channel_credentials)
    else:
        log.debug("Creating insecure gRPC channel")
        channel = grpc.insecure_channel(args.serverUrl)

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
    log.debug(f">>>> Start Request: {start_req}")
    start_response, call = stub.Start.with_call(start_req)
    response = MessageToDict(start_response)
    log.debug(f'<<<< Start Request Response: {json.dumps(response, indent=2)}')
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
    log.debug(f'>>>> Execute Request: {execute_request}')
    execute_response, call = stub.Execute.with_call(execute_request)
    response = MessageToDict(execute_response)
    log.debug(f'<<<< Execute Response: {json.dumps(response, indent=2)}')
    return response, call

def stop_request(stub, session_id=None):
    stop_req = StopRequest(session_id=session_id)
    log.debug(f'Stop Request: {stop_req}')
    stop_response, call = stub.Stop.with_call(stop_req)
    response = MessageToDict(stop_response)
    log.debug(f'Stop Response: {response}')
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
    log.debug(f"data access -> {data_action}")
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
            viz_prompt = ''.join([x['text'] for x in action['prompt']['visual']])
            print(f"{blue_bold('System >')} {blue(viz_prompt)}")
        elif "data" in action:
            data_action = action['data'] # TODO: review
    if data_action is not None:
        return process_data_request(data_action)
    return None

def main():
    args = parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        format='%(asctime)s %(levelname)-5s: %(message)s', level=log_level)
    with create_channel(args) as channel:
        stub = ChannelConnectorServiceStub(channel)
        selector_dict = {
            "channel": "web",
            "language": "en-US",
            "library": "default"
        }
        response, call = start_request(stub, 
                            model_ref=args.modelUrn, 
                            session_id=str(uuid.uuid1()), # Create a session id
                            selector_dict=selector_dict
                        )
        session_id = read_session_id_from_response(response)
        log.debug(f'Session: {session_id}')
        print(f'Session: {session_id}\n')
        assert call.code() == StatusCode.OK

        inited = False
        data_action = None

        try:
            while True:
                payload_dict = {}
                if data_action is None:
                    user_text = input(cyan_bold('User > ')) if inited else None
                    payload_dict = {"input": {}}
                    if user_text is not None:
                        payload_dict['input'].update({
                            "userText": user_text
                        })
                response, call = execute_request(stub, 
                                    session_id=session_id, 
                                    selector_dict=selector_dict,
                                    payload_dict=payload_dict,
                                    data_action=data_action
                                )
                data_action = handle_response(response)
                inited = True
        except KeyError:
            print("x ..wrapping up..")
        except Exception as e:
            log.exception(e)
        finally:
            assert call.code() == StatusCode.OK
            response, call = stop_request(stub, 
                                session_id=session_id
                            )
            assert call.code() == StatusCode.OK
            sys.exit(2)


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
