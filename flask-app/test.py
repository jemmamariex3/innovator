

from google.api.api_python import *
# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C599/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjUyMjc4MiwiZXh0Ijp7fSwiaWF0IjoxNTc2NTE5MTgyLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiYzFiODNlMTAtMjJjYy00YjM2LWFmYWYtNTNjYjc4ZDUyZWM3IiwibmJmIjoxNTc2NTE5MTgyLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.DXU5f8pFlHk9ynyFxAkVaAss9H56WiKeKKkzYR3g66QvxiBzafd4NN8zCC-RAeVnK1huW_PDjRHHrGySfFxKIVFPe0slNBJPVVAegzNtcPv7hpEyahIMVd5f1biQSyercFlLlS09baWy7lDoLuhu97qZ-CsxhfU-VP2M1m31VPNXsVeouWD05hSTwc7Mt1wlATE_IzV0s1TO7X8HIxnUo4oj8KEZGXRi0Idr2-KTZHOgnzDrpTYejSNKuaQGGR9bOP2tsYEzcw5rg_vzvFMTIivO0xapuAhOyBu9qXYOYMi0jR9OK10LlUKTKVHTaC6VlXFeZU6DmJOxCbAChH14XPEi1_VY6Qug-izdVkLcehmoT-I0gqGJT3KBT3vGpt4KFtR4NHOto7sXEgNrrUJmjjMmjzRjhUH0tR94rnKWl_Gc6d4fMR-MMFKU551MG0lqmtdI-Iq07_mRXDpQlY1Yph0a104ctxe0Tkm0I639ynFFlcucHZVZcOkE9suvTZNDx8khgnmdGy-5H9SIzkTquoJ9bG_VLS4qgA1eSm6b9-LheuZx-fAc6Hqc9xHd6hgse_PJgt-n9UXB9ebEmG8YmoVBNFTFmIqBnBqnD9IBRS9bhJxQPvzKzmvwYPK-2_pcYCiQLA0eVkSd16IR8Abd2UAd-VI15FopdA_uglVcSDw"
serverUrl = "dlgaas.beta.mix.nuance.com:443"
textInput = "test"

channel = create_channel(token, serverUrl)
stub = ChannelConnectorServiceStub(channel)
selector_dict = {
            "channel": "smartspeakerva",
            "language": "en-US",
            "library": "default"
}
session_id = ''
data_id = ''
data_values = {}
response_ticketsArr = []
userText = "Show me the open tickets"

ticketsArr = [
    { 'number': 1, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'Verizon', 'summary': "Register team in mix", 'hoursLogged': 8, 'priority': "high", 'status': 'open' },
    { 'number': 2, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'AT&T', 'summary': "Register teamz in mix", 'hoursLogged': 2, 'priority': "low", 'status': 'open' },
    { 'number': 3, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'Sprint', 'summary': "Register teamzzz in mix", 'hoursLogged': 3, 'priority': "medium", 'status': 'open' },
]

def filter_tickets(option, values):
    if option is "TD":
        print("yes, here is ticket data")
    elif option is "TAD":
        print("yes, here is the assignee")
    elif option is "TBAD":
        print("yes, here are all the tickets from assignee")
    elif option is "TBPD":
        print("yes here are tickets by 'priority':")
    elif option is "TBSD":
        if("_concept_TICKET_STATUS" in values):
            for ticket in ticketsArr:
                if ticket['status'] is 'open':
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
                
            print(final_response)
    elif option is "TBCD":
        print("woo, here are tickets by client")
    elif option is "TBCAD":
        print("here are tickets by client + assignee")
    elif option is "TBCPD":
        print("here are tickets by client + 'priority':")
    elif option is "TBCPAD":
        print("here are tickets by client, 'priority':, assignee")
    elif option is "TBSAD":
        print("here are tickets by status + assignee")
    elif option is "TBSCD":
        print("here are tickets by status+client")
    elif option is "TBSCAD":
        print("here are tickets by status + client + assignee"),
    elif option is "TBSCPD":
        print ("here are tickets by status+client+'priority':")
    elif option is "TBSCPAD":
        print("here are tickets by status, client, 'priority':, assignee")
    elif option is "TBSPD":
        print("here are tickets by status, 'priority':")
    elif option is "TBSPAD":
        print("here are tickets by status, 'priority':, assignee")
    elif option is "TCOD":
        print("here are tickets by comment")
    elif option is "TDD":
        print("here are ticket dates")
    elif option is "TPD":
        print("here is ticket 'priority': data")
    elif option is "TSD":
        print("here is ticket status data")
    elif option is "TBPAD":
        print("here is ticket by priority assignee")
    elif option is "MTCAD":
        print("modify ticket: change assignee data"),
    elif option is "MTCEDD":
        print("modify ticket: change end date data")
    elif option is "MTCPD":
        print("modify ticket: change 'priority': data")
    elif option is "MTCSD":
        print("modify ticket: change status data")
    elif option is "MTLHD":
        print("modify ticket: log hours data")
    elif option is "MTACD":
        print("modify ticket: add comment data")
    elif option is "MTCSD":
        print("modify ticket: change status data")
    return "success"

def filter_intents(i):
    intentSwitcher={
        "GetTicketData":'TD',
        "GetTicketAssigneeData":'TAD',
        "GetTicketByAssigneeData":'TBAD',
        "GetTicketByPriorityAssigneeData": 'TBPAD',
        "GetTicketByPriorityData":'TBPD',
        "GetTicketByStatusData":'TBSD',
        "GetTicketByClientData":'TBCD',
        "GetTicketByClientAssigneeData":'TBCAD',
        "GetTicketByClientPriorityData":'TBCPD',
        "GetTicketByClientPriorityAssigneeData":'TBCPAD',
        "GetTicketByStatusAssigneeData":'TBSAD',
        "GetTicketByStatusClientData":'TBSCD',
        "GetTicketByStatusClientAssigneeData":'TBSCAD',
        "GetTicketByStatusClientPriorityData":'TBSCPD',
        "GetTicketByStatusClientPriorityAssigneeData":"TBSCPAD",
        "GetTicketByStatusPriorityData":"TBSPD",
        "GetTicketByStatusPriorityAssigneeData":"TBSPAD",
        "GetTicketCommentsData":"TCOD",
        "GetTicketDatesData":"TDD",
        "GetTicketPriorityData":"TPD",
        "GetTicketStatusData":"TSD",
        "ModifyTicketChangeAssigneeData":"MTCAD",
        "ModifyTicketChangeEndDateData":"MTCEDD",
        "ModifyTicketChangePriorityData":"MTCPD",
        "ModifyTicketChangeStatusData":"MTCSD",
        "ModifyTicketLogHoursData":"MTLHD",
        "ModifyTicketAddCommentData": "MTACD",
        "ModifyTicketChangeStatusData": "MTCSD"
    }
    return intentSwitcher.get(i,"did not match any intent")


def start_chat():
    global session_id
    global userText
    global data_values
    response, call = start_request(stub, 
                            model_ref=modelUrn, 
                            session_id=str(uuid.uuid1()), # Create a session id
                            selector_dict=selector_dict
                        )
    session_id = read_session_id_from_response(response)
    #log.debug(f'Session: {session_id}')
    #assert call.code() == StatusCode.OK
    print("started the request. This is the session_id: ", session_id)
    print("This is the initial start response: ", response)
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
    print("This is the va response: ", va_response)
    message_array = []
    for prompts in va_response["action"]:
        for message in prompts["prompt"]["visual"]:
            message_array.append(message["text"])
    #response, call = stop_request(stub, session_id=session_id)
    #assert call.code() == StatusCode.OK
    print("This is all the messages", message_array)
    return

def continue_chat(): 
    global session_id
    global data_id
    global data_values
    print("This is the session_id (in continue_chat()): ", session_id) 
    payload_dict = {
            "input": {
                "userText": userText
            }
    }
    response, call = execute_request(stub, 
                            session_id=session_id, 
                            selector_dict=selector_dict,
                            payload_dict=payload_dict
                        )    
    print("this is before payload", response)
    va_response = response["payload"]
    va_action = va_response["action"]
    for item in va_action:
        if "data" in item:
            intent = filter_intents(item["data"]["id"])
            data_values = item["data"]["value"]
            filter_tickets(intent,data_values)


    print("This is the va response: ", va_response)
    message_array = []
    print("going to end it now")
    response, call = stop_request(stub, session_id=session_id)
    assert call.code() == StatusCode.OK
    return
"""     for action in va_response["action"]:
        if "prompt" in action:
            for message in action["prompt"]["visual"]:
                message_array.append(message["text"])
        elif "data" in action:
            data_id = action["data"]["id"]
            data_values = action["data"]["value"]
            for value in data_values:
                data_values[value] = 5
            payload_dict = { 
                "value": data_values
            }
            response, call = execute_request(stub, 
                            session_id=session_id, 
                            selector_dict=selector_dict,
                            payload_dict=payload_dict
                        )
            va_response = response["payload"]
            message_array = []  """    
    
    #jsonify(userText=''.join(message_array))  


start_chat()
continue_chat()



"""
GetTicketData == This will send TICKET_NUMBER
GetTicketAssigneeData TICKET_NUMBER ##Return assignee
GetTicketByAssigneeData TICKET_ASSIGNEE ##Return tickets 
GetTicketByPriorityData TICKET_PRIORTY
GetTicketByStatusData  TICKET_STATUS
GetTicketByClientData  TICKET_CLIENT
GetTicketByClientAssigneeData TICKENT_CLIENT  TICKET_ASSIGNEE
GetTicketByClientPriorityData      TICKET_CLIENT  TICKET_PRIORITY
GetTicketByClientPriorityAssigneeData   TICKET_CLIENT TICKET_ASSIGNEE TICKET_PRIORITY
GetTicketByStatusAssigneeData   TICKET_ASSIGNEE TICKET_STATUS
GetTicketByStatusClientData     TICKET_CLIENT  TICKET_STATUS
GetTicketByStatusClientAssigneeData TICKET_CLIENT, TICKET_ASSIGNEE, TICKET_STATUS
GetTicketByStatusClientPriorityData TICKET_STATUS, TICKET_CLIENT, TICKET_PRIORITY
GetTicketByStatusClientPriorityAssigneeData TICKET_ASSIGNEE, TICKET_CLIENT, TICKET_STATUS, TICKET_PRIORITY
GetTicketByStatusPriorityData   TICKET_STATUS, TICKET_PRIORITY
GetTicketByStatusPriorityAssigneeData   TICKET_STATUS TICKET_PRIORITY TICKET_ASSIGNEE
GetTicketCommentsData       TICKET_NUMBER
GetTicketDatesData          TICKET_NUMBER
GetTicketPriorityData   TICKET_NUMBER
GetTicketStatusData     TICKET_NUMBER
GetTicketByPriorityAssigneeData    TICKET_PRIORITY TICKET_ASSIGNEE
ModifyTicketChangeAssigneeData      TICKET_ASSIGNEE TICKET_NUMBER
ModifyTicketChangeEndDateData       TICKET_NUMBER  TICKET_END_DATE
ModifyTicketChangePriorityData      TICKET_NUMBER TICKET_PRIORITY
ModifyTicketChangeStatusData   TICKET_NUMBER TICKET_STATUS
ModifyTicketLogHoursData    TICKET_NUMBER TICKET_HOURS_LOGGED
ModifyTicketAddCommentData  TICKET_NUMBER TICKET_COMMENT







{'action': [{'data': {'id': 'GetTicketByStatusData'}}]}
"""