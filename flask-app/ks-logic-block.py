ticketsArr = [
	{
		"number": "10001",
		"summary": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
		"client": "Verizon",
		"priority": "low",
		"status": "open",
		"createdDate": "12/12/19",
		"startDate": "12/13/19",
		"endDate": "12/15/19",
		"assignee": "DaLarm Han",
		"hoursLogged": "0",
		"comments": "Lacus vestibulum sed arcu non odio."
	},
	{
		"number": "10002",
		"summary": "Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
		"client": "Sprint",
		"priority": "medium",
		"status": "in progress",
		"createdDate": "12/13/19",
		"startDate": "12/14/19",
		"endDate": "12/16/19",
		"assignee": "Peter Chea",
		"hoursLogged": "1",
		"comments": "Sociis natoque penatibus et magnis dis parturient montes nascetur. "
	},
	{
		"number": "10003",
		"summary": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. ",
		"client": "ATT",
		"priority": "high",
		"status": "complete",
		"createdDate": "12/14/19",
		"startDate": "12/15/19",
		"endDate": "12/17/19",
		"assignee": "Jemma Tiongson",
		"hoursLogged": "2",
		"comments": "Nisi lacus sed viverra tellus in. Convallis posuere morbi leo urna molestie at elementum eu."
	},
	{
		"number": "10004",
		"summary": "Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.",
		"client": "Costco",
		"priority": "low",
		"status": "closed",
		"createdDate": "12/15/19",
		"startDate": "12/16/19",
		"endDate": "12/18/19",
		"assignee": "Kevin Rickard",
		"hoursLogged": "2.5",
		"comments": "At auctor urna nunc id cursus. "
	},
	{
		"number": "10005",
		"summary": "Integer enim neque volutpat ac tincidunt.",
		"client": "Verizon",
		"priority": "medium",
		"status": "open",
		"createdDate": "12/16/19",
		"startDate": "12/17/19",
		"endDate": "12/19/19",
		"assignee": "DaLarm Han",
		"hoursLogged": "0",
		"comments": "Egestas erat imperdiet sed euismod."
	},
	{
		"number": "10006",
		"summary": "Aliquam faucibus purus in massa tempor.",
		"client": "Sprint",
		"priority": "high",
		"status": "in progress",
		"createdDate": "12/17/19",
		"startDate": "12/18/19",
		"endDate": "12/20/19",
		"assignee": "DaLarm Han",
		"hoursLogged": "1",
		"comments": "Est lorem ipsum dolor sit amet consectetur."
	},
	{
		"number": "10007",
		"summary": "Lacus vestibulum sed arcu non odio.",
		"client": "ATT",
		"priority": "low",
		"status": "complete",
		"createdDate": "12/18/19",
		"startDate": "12/19/19",
		"endDate": "12/21/19",
		"assignee": "Peter Chea",
		"hoursLogged": "2",
		"comments": "Arcu vitae elementum curabitur vitae nunc sed velit."
	},
	{
		"number": "10008",
		"summary": "Sociis natoque penatibus et magnis dis parturient montes nascetur. ",
		"client": "Costco",
		"priority": "medium",
		"status": "closed",
		"createdDate": "12/19/19",
		"startDate": "12/20/19",
		"endDate": "12/22/19",
		"assignee": "Jemma Tiongson",
		"hoursLogged": "2.5",
		"comments": "Libero justo laoreet sit amet cursus sit amet dictum sit."
	},
	{
		"number": "10009",
		"summary": "Nisi lacus sed viverra tellus in. Convallis posuere morbi leo urna molestie at elementum eu.",
		"client": "Verizon",
		"priority": "high",
		"status": "open",
		"createdDate": "12/20/19",
		"startDate": "12/21/19",
		"endDate": "12/23/19",
		"assignee": "Kevin Rickard",
		"hoursLogged": "0",
		"comments": "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
	},
	{
		"number": "10010",
		"summary": "At auctor urna nunc id cursus. ",
		"client": "Sprint",
		"priority": "low",
		"status": "in progress",
		"createdDate": "12/21/19",
		"startDate": "12/22/19",
		"endDate": "12/24/19",
		"assignee": "DaLarm Han",
		"hoursLogged": "1",
		"comments": "Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
	},
	{
		"number": "10011",
		"summary": "Egestas erat imperdiet sed euismod.",
		"client": "ATT",
		"priority": "medium",
		"status": "complete",
		"createdDate": "12/22/19",
		"startDate": "12/23/19",
		"endDate": "12/25/19",
		"assignee": "DaLarm Han",
		"hoursLogged": "2",
		"comments": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
	},
	{
		"number": "10012",
		"summary": "Est lorem ipsum dolor sit amet consectetur.",
		"client": "Costco",
		"priority": "high",
		"status": "closed",
		"createdDate": "12/23/19",
		"startDate": "12/24/19",
		"endDate": "12/26/19",
		"assignee": "Peter Chea",
		"hoursLogged": "2.5",
		"comments": "Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum."
	},
	{
		"number": "10013",
		"summary": "Arcu vitae elementum curabitur vitae nunc sed velit.",
		"client": "Verizon",
		"priority": "low",
		"status": "open",
		"createdDate": "12/24/19",
		"startDate": "12/25/19",
		"endDate": "12/27/19",
		"assignee": "Jemma Tiongson",
		"hoursLogged": "0",
		"comments": "Integer enim neque volutpat ac tincidunt."
	},
	{
		"number": "10014",
		"summary": "Libero justo laoreet sit amet cursus sit amet dictum sit.",
		"client": "Sprint",
		"priority": "medium",
		"status": "in progress",
		"createdDate": "12/25/19",
		"startDate": "12/26/19",
		"endDate": "12/28/19",
		"assignee": "Kevin Rickard",
		"hoursLogged": "1",
		"comments": "Aliquam faucibus purus in massa tempor."
	},
	{
		"number": "10015",
		"summary": "Augue eget arcu dictum varius duis at consectetur lorem.",
		"client": "ATT",
		"priority": "high",
		"status": "complete",
		"createdDate": "12/26/19",
		"startDate": "12/27/19",
		"endDate": "12/29/19",
		"assignee": "DaLarm Han",
		"hoursLogged": "2",
		"comments": "Augue eget arcu dictum varius duis at consectetur lorem."
	},
	{
		"number": "10016",
		"summary": "A erat nam at lectus urna. ",
		"client": "Costco",
		"priority": "low",
		"status": "closed",
		"createdDate": "12/27/19",
		"startDate": "12/28/19",
		"endDate": "12/30/19",
		"assignee": "DaLarm Han",
		"hoursLogged": "2.5",
		"comments": "A erat nam at lectus urna. "
	},
	{
		"number": "10017",
		"summary": "Nulla pharetra diam sit amet nisl. ",
		"client": "Verizon",
		"priority": "medium",
		"status": "open",
		"createdDate": "12/28/19",
		"startDate": "12/29/19",
		"endDate": "12/31/19",
		"assignee": "Peter Chea",
		"hoursLogged": "0",
		"comments": "Nulla pharetra diam sit amet nisl. "
	},
	{
		"number": "10018",
		"summary": "Massa vitae tortor condimentum lacinia quis vel eros donec.",
		"client": "Sprint",
		"priority": "high",
		"status": "in progress",
		"createdDate": "12/29/19",
		"startDate": "12/30/19",
		"endDate": "01/01/20",
		"assignee": "Jemma Tiongson",
		"hoursLogged": "1",
		"comments": "Massa vitae tortor condimentum lacinia quis vel eros donec."
	},
	{
		"number": "10019",
		"summary": "Pellentesque diam volutpat commodo sed egestas.",
		"client": "ATT",
		"priority": "high",
		"status": "complete",
		"createdDate": "12/30/19",
		"startDate": "12/31/19",
		"endDate": "01/02/20",
		"assignee": "Kevin Rickard",
		"hoursLogged": "2",
		"comments": "Pellentesque diam volutpat commodo sed egestas."
	}
]
response_ticketsArr = []

def filter_tickets(option, values):
    global userText
    # Get Tickets
    if option is "TD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    final_response = ("Ticket #" + ticket['number'] + "\nSummary: " + ticket['summary'] + "\nClient: " + ticket['client'] + "\nPriority: " + ticket['priority'] + "\nStatus: " + ticket['status'] + "\nAssignee: " + ticket['assignee'] + "\nHours Logged: " + ticket['hoursLogged'])
                    break
            print(option + " - final response: " + final_response)
    elif option is "TDD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    final_response = ("Created Date: " + ticket['createdDate'] + "\nStart Date: " + ticket['startDate'] + "\nEnd Date: " + ticket['endDate'])
                    break
            print(option + " - final response: " + final_response)
    elif option is "TAD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    final_response = (ticket['assignee'])
                    break
            print(option + " - final response: " + final_response)
    elif option is  "TPD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    final_response = (ticket['priority'])
                    break
            print(option + " - final response: " + final_response)
    elif option is "TSD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    final_response = (ticket['status'])
                    break
            print(option + " - final response: " + final_response)
    elif option is "TCOD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    final_response = (ticket['comments'])
                    break
            print(option + " - final response: " + final_response)
    # Modify Tickets - no return
    elif option is "MTCAD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    # MODIFY ASSIGNEE CODE HERE
                    final_response = (ticket)
                    break
            print(option + " - final response: " + final_response)
    elif option is "MTCPD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    # MODIFY PRIORITY CODE HERE
                    final_response = (ticket)
                    break
            print(option + " - final response: " + final_response)
    elif option is "MTCSD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    # MODIFY STATUS CODE HERE
                    final_response = (ticket)
                    break
            print(option + " - final response: " + final_response)
    elif option is "MTLHD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    # MODIFY HOURS LOGGED CODE HERE
                    final_response = (ticket)
                    break
            print(option + " - final response: " + final_response)
    elif option is "MTACD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is int(ticket_num):
                    # MODIFY COMMENT CODE HERE
                    final_response = (ticket)
                    break
            print(option + " - final response: " + final_response)
    # Get Tickets By
    elif option is "TBAD":
        print("intent = " + option)
        if("concept_TICKET_ASSIGNEE" in values):
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBPD":
        print("intent = " + option)
        if("concept_TICKET_PRIORITY" in values):
            priority = values["_concept_TICKET_PRIORITY"]
            for ticket in ticketsArr:
                if (ticket['priority'] == priority):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values):
            status = values["_concept_TICKET_STATUS"]
            for ticket in ticketsArr:
                if (ticket['status'] == status):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBCD":
        print("intent = " + option)
        if("concept_TICKET_CLIENT" in values):
            client = values["_concept_TICKET_CLIENT"]
            for ticket in ticketsArr:
                if (ticket['client'] == client):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBCAD":
        print("intent = " + option)
        if("concept_TICKET_CLIENT" in values and "concept_TICKET_ASSIGNEE" in values):
            client = values["_concept_TICKET_CLIENT"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['client'] == client and ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBCPD":
        print("intent = " + option)
        if("concept_TICKET_CLIENT" in values and "concept_TICKET_PRIORITY" in values):
            client = values["_concept_TICKET_CLIENT"]
            priority = values["_concept_TICKET_PRIORITY"]
            for ticket in ticketsArr:
                if (ticket['client'] == client and ticket['priority'] == priority):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBCPAD":
        print("intent = " + option)
        if("concept_TICKET_CLIENT" in values and "concept_TICKET_PRIORITY" in values and "concept_TICKET_ASSIGNEE" in values):
            client = values["_concept_TICKET_CLIENT"]
            priority = values["_concept_TICKET_PRIORITY"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['client'] == client and ticket['priority'] == priority and ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSAD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values and "concept_TICKET_ASSIGNEE" in values):
            status = values["_concept_TICKET_STATUS"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['status'] == status and ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSCD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values and "concept_TICKET_CLIENT" in values):
            status = values["_concept_TICKET_STATUS"]
            client = values["_concept_TICKET_CLIENT"]
            for ticket in ticketsArr:
                if (ticket['status'] == status and ticket['client'] == client):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSCAD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values and "concept_TICKET_CLIENT" in values and "concept_TICKET_ASSIGNEE" in values):
            status = values["_concept_TICKET_STATUS"]
            client = values["_concept_TICKET_CLIENT"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['status'] == status and ticket['client'] == client and ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSCPD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values and "concept_TICKET_CLIENT" in values and "concept_TICKET_PRIORITY" in values):
            status = values["_concept_TICKET_STATUS"]
            client = values["_concept_TICKET_CLIENT"]
            priority = values["_concept_TICKET_PRIORITY"]
            for ticket in ticketsArr:
                if (ticket['status'] == status and ticket['client'] == client and ticket['priority'] == priority):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSCPAD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values and "concept_TICKET_CLIENT" in values and "concept_TICKET_PRIORITY" in values and "concept_TICKET_ASSIGNEE" in values):
            status = values["_concept_TICKET_STATUS"]
            client = values["_concept_TICKET_CLIENT"]
            priority = values["_concept_TICKET_PRIORITY"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['status'] == status and ticket['client'] == client and ticket['priority'] == priority and ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSPD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values and "concept_TICKET_PRIORITY" in values):
            status = values["_concept_TICKET_STATUS"]
            priority = values["_concept_TICKET_PRIORITY"]
            for ticket in ticketsArr:
                if (ticket['status'] == status and ticket['priority'] == priority):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBSPAD":
        print("intent = " + option)
        if("concept_TICKET_STATUS" in values and "concept_TICKET_PRIORITY" in values and "concept_TICKET_ASSIGNEE" in values):
            status = values["_concept_TICKET_STATUS"]
            priority = values["_concept_TICKET_PRIORITY"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['status'] == status and ticket['priority'] == priority and ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    elif option is "TBPAD":
        print("intent = " + option)
        if("concept_TICKET_PRIORITY" in values and "concept_TICKET_ASSIGNEE" in values):
            priority = values["_concept_TICKET_PRIORITY"]
            assignee = values["_concept_TICKET_ASSIGNEE"]
            for ticket in ticketsArr:
                if (ticket['priority'] == priority and ticket['assignee'] == assignee):
                    response_ticketsArr.append("#" + ticket['number'])
                    final_response = ', '.join(map(str,response_ticketsArr))
            print(option + " - final response: " + final_response)
    return final_response

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
        "ModifyTicketChangePriorityData":"MTCPD",
        "ModifyTicketChangeStatusData":"MTCSD",
        "ModifyTicketLogHoursData":"MTLHD",
        "ModifyTicketAddCommentData": "MTACD",
    }
    return intentSwitcher.get(i,"did not match any intent")