

from google.api.api_python import *
# API-related info
modelUrn = "urn:nuance:mix/eng-USA/A174_C599/mix.dialog"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3NjUzNTk4MiwiZXh0Ijp7fSwiaWF0IjoxNTc2NTMyMzgyLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiYjQwY2ExOGMtYmFkZC00MWUyLWEwZmEtMjc2NTBiNmU4MWZjIiwibmJmIjoxNTc2NTMyMzgyLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.Fz9tiV_5exA1GUEPs3itGgy7CnXS1kkaJYtI4RfdUL8TXVJ-mltKOtIeUaBHwiLmD9oqjXsUPlKoPxIzMB-xTB7Xt_vYjx8OWU1-Cf1N7UrcdJYXyCybH2Js1Mw8n36GVbwJMYjdT8uhg-EEiU8B7_T8ruAlBIfvy5L6pc95EV_KdY2-DnwK0brJEM6UPt2QypwPeRNpTPSGgB8ypWKoM3sDs2YIFbKSQnnm76D0Qf2OAIPDK5DPG6ENeQOG7jwneRhb6bZAXUk4JCnMzqhL6DcYOeH0vK2bMZ3umrXCTHstosHkneNqkI91T_mbGBtbxtnOC-ImkL95jFMpzsqysfx1iH6lzNJsrGAhytCjJ-gfEVtPkb6q111FgspLWEN5w1IuzPoIE2uSw3hlcq3l9LBWadSbCrZuCKyLYl11N9NuxRE26Xb-OfLmdKfA12EUOjKNqO0raShxr48zLgpeXUCo0FofZZq8Ws-JegDIZr9fQMbR2G0o8rBluATzqwVoPTIsZvlQekbzHWxaXd9TwUj3osF4FwTLLe2mqvm_2UL-3PtEZOhq0KxeQHIzr31wxXXou_EXMagL-Sdk4YvE4xufb3qOLsQmNFOLRby3okpR-KpeptdXQlpvAYegjpOvcq3TW-8AqHf-ILgT_MOUAaLYTTwQsIqE5UWkfkdFeuc"
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
userText = "Does dalarm have open verizon tickets of high importance?"

ticketsArr = [
    { 'number': 1, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'Verizon', 'summary': "Register team in mix", 'hoursLogged': 8, 'priority': "high", 'status': 'open' },
    { 'number': 2, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'AT&T', 'summary': "Register teamz in mix", 'hoursLogged': 2, 'priority': "low", 'status': 'open' },
    { 'number': 3, 'assignee': "DaLarm Han", 'dueDate': "12/19/2019", 'client': 'Sprint', 'summary': "Register teamzzz in mix", 'hoursLogged': 3, 'priority': "medium", 'status': 'open' },
]

def filter_tickets(option, values):
    if option is "TD":
        print("yes, here is ticket data")
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    response_ticketsArr.append(ticket)
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TAD":
        print("yes, here is the assignee")
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    response_ticketsArr.append(ticket['assignee'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBAD":
        print("yes, here are all the tickets from assignee")
        if("_concept_TICKET_ASSIGNEE" in values):
            # print(values['_concept_TICKET_ASSIGNEE'])
            assignee = values["_concept_TICKET_ASSIGNEE"]
            # for ticket in ticketsArr:
            #     if ticket['status'] is '':
            #         response_ticketsArr.append(ticket['number'])
            #         final_response = ''.join(map(str,response_ticketsArr))
            # print("Final response: " + final_response)
    elif option is "TBPD":
        print("yes here are tickets by 'priority':")
    elif option is "TBSD":
        print("here are tickets by status")
        if("_concept_TICKET_STATUS" in values):
            for ticket in ticketsArr:
                if ticket['status'] is 'open':
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBCD":
        print("woo, here are tickets by client")
        if("_concept_TICKET_CLIENT" in values):
            client = values["_concept_TICKET_CLIENT"]
            for ticket in ticketsArr:
                if ticket['client'] == client:
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBCAD":
        print("here are tickets by client + assignee")
        if("_concept_TICKET_CLIENT" in values and "_concept_TICKET_ASSIGNEE" in values):
            client = values["_concept_TICKET_CLIENT"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['client'] == client and ticket['assignee'] == assignee):
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBCPD":
        print("here are tickets by client + 'priority':")
        if("_concept_TICKET_CLIENT" in values and "_concept_TICKET_PRIORITY" in values and  "_concept_TICKET_ASSIGNEE" in values):
            client = values["_concept_TICKET_CLIENT"]
            priority = values["concept_TICKET_PRIORITY"]
            for ticket in ticketsArr: 
                if (ticket['client'] == client and ticket['priority'] == priority):
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBCPAD":
        print("here are tickets by client, 'priority':, assignee")
        if("_concept_TICKET_CLIENT" in values and "_concept_TICKET_PRIORITY" in values and  "_concept_TICKET_ASSIGNEE" in values):
            client = values["_concept_TICKET_CLIENT"]
            priority = values["_concept_TICKET_PRIORITY"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr: 
                if (ticket['client'] == client and ticket['priority'] == priority and ticket['assignee'] == assignee):
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBSAD":
        print("here are tickets by status + assignee")
        if("_concept_TICKET_STATUS" in values and  "_concept_TICKET_ASSIGNEE" in values):
            status = values["_concept_TICKET_STATUS"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr: 
                if (ticket['status'] == status and ticket['assignee'] == assignee):
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBSCD":
        print("here are tickets by status+client")
        if("_concept_TICKET_CLIENT" in values and "_concept_TICKET_STATUS" in values):
            client = values["_concept_TICKET_CLIENT"]
            status = values["_concept_TICKET_STATUS"]
            for ticket in ticketsArr: 
                if (ticket['client'] == client and ticket['status'] == status):
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBSCAD":
        print("here are tickets by status + client + assignee"),
        if("_concept_TICKET_CLIENT" in values and "_concept_TICKET_STATUS" in values and  "_concept_TICKET_ASSIGNEE" in values):
            client = values["_concept_TICKET_CLIENT"]
            status = values["_concept_TICKET_STATUS"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr: 
                if (ticket['client'] == client and ticket['status'] == status and ticket['assignee'] == assignee):
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
    elif option is "TBSCPD":
        print ("here are tickets by status+client+'priority':")
        if("_concept_TICKET_CLIENT" in values and "_concept_TICKET_STATUS" in values and  "_concept_TICKET_PRIORITY" in values):
            client = values["_concept_TICKET_CLIENT"]
            status = values["_concept_TICKET_STATUS"]
            priority = values["_concept_TICKET_PRIORITY"]
            for ticket in ticketsArr: 
                if (ticket['client'] == client and ticket['status'] == status and ticket['priority'] == priority):
                    response_ticketsArr.append(ticket['number'])
                    final_response = ''.join(map(str,response_ticketsArr))
            print("Final response: " + final_response)
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

def continue_chat_twice(): 
    global session_id
    global data_id
    global data_values
    print("This is the session_id (in continue_chat()): ", session_id) 
    payload_dict = {
        "input": {
            "userText": userText2
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
    # print("going to end it now")
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
# continue_chat_twice()



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