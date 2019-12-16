

from google.api.python-api-enh import *
# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C599/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjUzMzA2NywiZXh0Ijp7fSwiaWF0IjoxNTc2NTI5NDY3LCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiYmEyMGY5YzQtYTIxMi00OTM4LTg1YzQtNzA4OWEwNTg3NGY1IiwibmJmIjoxNTc2NTI5NDY3LCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.nJhA0QEy1zHggp8Uyb2mt13YdRsijIr-LULqHAMVvwfvDv2rYLAGMGfTslrB6kh1xvn6hP8WpWqBkyoomJGY_dVVgtz2ZN0a7EwaQ51DYgRE0_L9YLsSIKfe2lw2ccN5YqtysGj3ypsJaZo525HRiI6gfB3hFejqr2n7qg5kwwgt4_IhnNT09o7WTndziq62_XlNEETditEyKDH-xX65XMTgiQvjWqNvkEqd0nC7cNFJEMkpAEwWGS-hrtTzcPT3XD3PBXnzQobTduOIrc0250s3CiCBqg2aw3qxNkjHIYUVmN29-afPK_0CWyy3vewWhA-bOjT_X8-qVwiNN8_LgHf4ft71z34qq4DSKjebmcWGuJEu-2cRLI4oAGM7Vd9Mg-8m751r2nGlQTMWLtM3Xf9pT3POdDTMpt3SL-mDdL-wK8arYnwHpjvLlJnJIqOuKHNCtj-XM0yR5zHtFUgSnXzdZyWcAuQAOqgMJ-Ubw8FdAWLDlNoclIFU4I4a95MkbL3G0CkzYX9OlFG2XSJ_0tfNTIyt3vwrux8xZPd0cbRekiBH6r4cSm7qR0DO9WTrE6jPdpvoVgGzS0rUCONXgIulDSuWrQbwacwTDCG7wEB_U6UpSail9FR9SmlrRfQVpGdqtjFrZONwGRsT-ZLmUct3NX5426TyELawTfRUoak"
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
data_dict = {'data': {"id": "", "value":{}}}
userText = "Show me the open tickets"

ticketsArr = [
    { 'number': 1, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'Verizon', 'summary': "Register team in mix", 'hoursLogged': 8, 'priority': "high", 'status': 'open' },
    { 'number': 2, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'AT&T', 'summary': "Register teamz in mix", 'hoursLogged': 2, 'priority': "low", 'status': 'open' },
    { 'number': 3, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'Sprint', 'summary': "Register teamzzz in mix", 'hoursLogged': 3, 'priority': "medium", 'status': 'open' },
]

def filter_tickets(option, values):
    global userText
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
                    final_response = ','.join(map(str,response_ticketsArr))
            data_dict["data"]["id"] = "GetTicketByStatusData"
            data_dict["data"]["value"] = {"returnMessage":final_response, "returnCode":"0"} 
            continue_chat(data_dict)
            print(data_dict)
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
    elif option is  "TPD":
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
        print("modify ticket: log houment data")
    elif option is "MTCSD":
        print("modify ticket: change srs data")
    elif option is "MTACD":
        print("modify ticket: add comtatus data")
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

def continue_chat(payload_msg): 
    global session_id
    global data_id
    global data_values
    print("This is the session_id (in continue_chat()): ", session_id) 
    print("this is the payload info", payload_msg)
    payload_dict = payload_msg
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
payload_msg = {
            "input": {
                "userText": userText
            }
    }
continue_chat(payload_msg)



"""
GetTicketData == VA will send TICKET_NUMBER
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