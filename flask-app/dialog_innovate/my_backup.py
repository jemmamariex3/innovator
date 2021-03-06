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
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo4MzQ3Zjc3OS1hMDIxLTRlMzEtYTQ4ZC1iNWU1NjdjMzg2ZmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJhcHBJRDpOTURQVFJJQUxfZGFsYXJtX2hhbl9udWFuY2VfY29tXzIwMTkxMjAyVDE5MjQ1Nzk0MDkzNSIsImV4cCI6MTU3Njg0MTAzMSwiZXh0Ijp7fSwiaWF0IjoxNTc2ODM3NDMxLCJpc3MiOiJodHRwczovL2F1dGguY3J0Lm51YW5jZS5jb20vIiwianRpIjoiZDhkZWYwNjAtOTM3My00YjhjLWIzNGItYTEzYzE4ZWQwZDYxIiwibmJmIjoxNTc2ODM3NDMxLCJzY3AiOlsiZGxnIl0sInN1YiI6ImFwcElEOk5NRFBUUklBTF9kYWxhcm1faGFuX251YW5jZV9jb21fMjAxOTEyMDJUMTkyNDU3OTQwOTM1In0.RgNGeS4wBpctQY0OF5g2-Ys4lyLDFaMpj6ZjDaPiT4am66MyLjWhKFqTe5urXY64D4yRNGdVWoiiRk9_Rz-LcRClCRIskGn6P3mwFPdqHlkoUqq-9H27IjDuixIAFHoY4_SNBBtL5MxqmNes0RwbAcVDN8CpSmE8T8L5BGCHgSmLxwqynX35vPvdl4dhHWOjKPrK_OlJwrdKY-WPgIZffnwE-7WhXaone_lQyTnk25j2objB_cZ97m59G5zlNOlf0SaST2i2vkjKJ2w5t7ua0RM558QHBSOhvZpIBlH7cCVyB1qryVkKZEzkoyWBAKGi6Rga9ldEDmkmVaiYMgJFQ77ZY3RXOjTEpwVs0Guj5YRakZOZCpufVVfFS3fJxp1zRqNfnlPQLc1SBVj68x6q5wKYseHp2Lxb-diZbLPkY9xkQqrnJJaJ5eOFyCt0TSp2CJWNd4oQwBIgutqYX5quv8NUifQKRd9htYmN64Da39PgUNELdYrh-KKFVG-wvFpTKfa7d3b6GQK5ygDmi4dI0bmyM6ihBzpAg4VRVz-QbWUpKmaDDs4NWmeYsYEUnlJwOsa_iEl4YnHQ8-v_f76COOHaxHXJ5UQ6xHHkO5O8KEp4FwLhFuOc5RMuzJ_fizEWjIu_UTXWrL5aM4x2yOg-u1LsoEdXISWdAp61fybIKLc"
serverUrl = "dlgaas.beta.mix.nuance.com:443"

selector_dict = {
            "channel": "web",
            "language": "en-US",
            "library": "default"
}
#textInput = "test"  Use this if you want to hardcode messages.

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
        "comments": "Sociis natoque penatibus et magnis dis parturient montes nascetur. "
    },
    {
        "number": "10003",
        "summary": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. ",
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
        "comments": "At auctor urna nunc id cursus. "
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
        "summary": "Sociis natoque penatibus et magnis dis parturient montes nascetur. ",
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
        "summary": "At auctor urna nunc id cursus. ",
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
        "comments": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
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
        "summary": "A erat nam at lectus urna. ",
        "client": "Costco",
        "priority": "low",
        "status": "closed",
        "createdDate": "12/27/19",
        "startDate": "12/28/19",
        "endDate": "12/30/19",
        "assignee": "DaLarm Han",
        "hoursLogged": "2.5",
        "comments": "A erat nam at lectus urna. "
    },
    {
        "number": "10017",
        "summary": "Nulla pharetra diam sit amet nisl. ",
        "client": "Verizon",
        "priority": "medium",
        "status": "open",
        "createdDate": "12/28/19",
        "startDate": "12/29/19",
        "endDate": "12/31/19",
        "assignee": "Peter Chea",
        "hoursLogged": "0",
        "comments": "Nulla pharetra diam sit amet nisl. "
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
    final_response = ""
    # Get Tickets
    if option is "TD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values):
            final_response = ""
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            print("This is from eval of two values: ", ticket_num)
            for ticket in ticketsArr:
                print("this is the ticket number: ", ticket['number'])
                if ticket['number'] is ticket_num:
                    print("it came in here nice.")
                    final_response = ("Ticket #" + ticket['number'] + "\nSummary: " + ticket['summary'] + "\nClient: " + ticket['client'] + "\nPriority: " + ticket['priority'] + "\nStatus: " + ticket['status'] + "\nAssignee: " + ticket['assignee'] + "\nHours Logged: " + ticket['hoursLogged'])
                    response_ticketsArr.append(final_response)
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
                if ticket['number'] is ticket_num:
                    final_response = (ticket['assignee'])
                    print("This is the assignee: ", final_response)
                    response_ticketsArr.append(final_response)
                    break
            print(option + " - final response: " + final_response)
    elif option is  "TPD":
        print("intent = " + option)
        if("_concept_TICKET_NUMBER" in values): 
            ticket_num = (eval(values['_concept_TICKET_NUMBER'])['nuance_CARDINAL_NUMBER'])
            for ticket in ticketsArr:
                if ticket['number'] is ticket_num:
                    final_response = (ticket['priority'])
                    response_ticketsArr.append(final_response)
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
        if("_concept_TICKET_CLIENT" in values):
            final_response = ""
            client = values["_concept_TICKET_CLIENT"]
            for ticket in ticketsArr:
                print("These are the ticket clients: ", ticket['client'])
                if (ticket['client'] == client):
                    print("This is what i'm appending: ", ticket['number'])
                    response_ticketsArr.append("#" + ticket['number'])
                    #final_response = ', '.join(map(str,response_ticketsArr))
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

def clear_ticket_responses():
    global response_ticketsArr
    response_ticketsArr = []

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

def get_tickets_arr(): 
    return ticketsArr

class DataClass:

    """
    Each function is a DA node. Simply return the values.
    """

    global ticketsArr
    global response_ticketsArr

    @data_access_node
    def GetTicketByStatusData(self, data):
        entity = data['value']['_concept_TICKET_STATUS']
        for ticket in ticketsArr: 
            t_status = ticket['status'].lower() == entity.lower()
            ticket_num = ticket['number']
            if(t_status): 
                print('ticket has status of open: ', ticket_num)
                response_ticketsArr.append(ticket_num)
        final_msg = ' '.join(map(str,response_ticketsArr))
        clear_ticket_responses()
        return {
            "returnMessage": final_msg + "."
        }
    
    @data_access_node
    def GetTicketData(self, data):
        entity = data['value']['_concept_TICKET_NUMBER']
        intent = filter_intents("GetTicketData")
        print("This is the appreviation: ", intent)
        print("this is the data[value]: ", data['value'])
        filter_tickets(intent, data['value'])
        final_msg = ' '.join(map(str,response_ticketsArr))
        clear_ticket_responses()
        return{
            "returnMessage": final_msg + "."
        }

    @data_access_node
    def GetTicketAssigneeData(self, data):
        entity = data['value']['_concept_TICKET_NUMBER']
        intent = filter_intents("GetTicketAssigneeData")
        print("This is the appreviation: ", intent)
        print("this is the data[value]: ", data['value'])
        filter_tickets(intent, data['value'])
        final_msg = ' '.join(map(str,response_ticketsArr))
        clear_ticket_responses()
        return{
            "returnMessage": final_msg + "."
        }

    @data_access_node
    def GetTicketPriorityData(self,data):
        entity = data['value']['_concept_TICKET_NUMBER']
        intent = filter_intents("GetTicketPriorityData")
        print("This is the appreviation: ", intent)
        print("this is the data[value]: ", data['value'])
        filter_tickets(intent, data['value'])
        final_msg = ' '.join(map(str,response_ticketsArr))
        clear_ticket_responses()
        return{
            "returnMessage": final_msg + "."
        }

    @data_access_node
    def GetTicketByClientData(self,data):
        entity = data['value']['_concept_TICKET_CLIENT']
        intent = filter_intents("GetTicketByClientData")
        print("This is the appreviation: ", intent)
        print("this is the data[value]: ", data['value'])
        filter_tickets(intent, data['value'])
        final_msg = ' '.join(map(str,response_ticketsArr))
        clear_ticket_responses()
        return{
            "returnMessage": final_msg + "."
        }

data_class = DataClass()

if __name__ == '__main__':
    main()
