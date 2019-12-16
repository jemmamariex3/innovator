

from google.api.api_python import *
# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C598/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjUxNTk0MywiZXh0Ijp7fSwiaWF0IjoxNTc2NTEyMzQzLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiNWMwNTNhNDEtZGE5Ny00MzJmLTg0YTEtNWM1YmYyZWFlOTAwIiwibmJmIjoxNTc2NTEyMzQzLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.OpTxoyI_4REDanP_MXBnwNCv0sqenesGysj9M6IK9P4GpiQgAG5UvDJiZSPEdulvWFgob0x4OtgUbqRquq0MoahZ2blb9aM-zXVFWGVcRtC3NMJ8PgwVlshpXKV6XFmhwi6MsYJkoGPR4UDl_j4ZqWNdmdEawBwrNlxBd1QCzrLYVhR6AtIE75A7WMwoyYlVLucOwH0yDvrmxBOvB_xintcIJCw4ian79Tb87jErXj_9JpVMkUIHVDWips3kk8wvfVBnUHIwKR85fiPc2_Dz8jYe1Ogo-1LoKuE0w1O-_ZaUQnuMFTFqH4_W7dGtON0alzxTIPzsYpD9Yoi5m9jMW6Hgh9bb8EmA2p-8gV-P5mmDSRjJHZF42rygyELU3xI-rWMpKFN4fqZKmXcm154xsTQN00YOn3QuZfiYHoQnuNZ3UJ2-gu7wQ0E0IWj0ZPGsWoDSZbfW3fXzC4R4GUCgGbqGfS6pnAqDyQBG49_rFLfko4ZJNlyQi4z_TuQD09e5yj3pLDAefs5AHUXiN_J_ity0DVhRx_FPhjWYxhdrw9aPpNknabZZdlD2aE01mR_NXXq2lrtOxXp67aRcy_qWM9l-4Zj8WUBYxQahliHIQ51Hys3r_Tq5Dg6AeaZECWa6o9j_VHxnAA_K1r4IkCO74x6GfpUXB55wxnE8SHthG90"
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

ticketsArr = [
    { 'number': 1, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'summary': "Register team in mix", 'hoursLogged': 8, 'priority': "high" },
    { 'number': 2, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'summary': "Register teamz in mix", 'hoursLogged': 2, 'priority': "low" },
    { 'number': 3, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'summary': "Register teamzzz in mix", 'hoursLogged': 3, 'priority': "medium" },
]

def filter_tickets(option):
    if option is "TD":
        print("yes, here is ticket data")
    elif option is "TAD":
        print("yes, here is the assignee")
    elif option is "TBAD":
        print("yes, here are all the tickets from assignee")
    elif option is "TBPD":
        print("yes here are tickets by 'priority':")
    elif option is "TBSD":
        print("yes here are tickets by status")
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
                "userText": "Show me the open tickets"
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
            filter_tickets(intent)


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