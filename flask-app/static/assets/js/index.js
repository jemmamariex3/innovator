// With CSS loader, we can import the css in the main JS file, rather than the html file
//import "../css/styles.css";
//import Ticket from "./Ticket.js";
// import { configs } from './key';

// const token = require("../../dialog_proto/token_scripts/my-token.json");
// console.log("Hi, this is our key object: ", configs);
// console.log("Token json: ", token);

class Ticket {
    constructor(number, assignee, dueDate, client, summary, hoursLogged, comments, priority = "low", status = "open", startDate = new Date()) {
        this.number = number;
        this.assignee = assignee;
        this.dueDate = dueDate;
        this.client = client;
        this.summary = summary;
        this.hoursLogged = hoursLogged;
        this.comments = comments; 
        this.priority = priority;
        this.status = status;
        this.startDate = startDate;
    }

    getTicketInfo() {
        const {...params } = this;

        return params;
    }
}

// Chat button logic
function addChatClick() {
    const chatContainer = document.querySelector(".right_container");
    const minimizeBtn = document.querySelector(".section_minimize");
    const closeBtn = document.querySelector(".section_close");

    minimizeBtn.addEventListener("click", (e) => {
        chatContainer.classList.toggle("minimize");
        chatContainer.classList.remove("close");
        console.log("current target for minimize btn: ", e.currentTarget);
    })

    closeBtn.addEventListener("click", (e) => {
        chatContainer.classList.toggle("close");
        chatContainer.classList.remove("minimize");
        console.log("current target for close btn: ", e.currentTarget);
    })
}

//////////////////// Accordion JS Start //////////////////
function addAccordionClick() {

    let acc = document.getElementsByClassName("accordion");

    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            let panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
}
////////////////// Accordion JS End ////////////////////

////////////////// Populate Accordion Start //////////////////
// const ticketsArr = [
//     { number: 1, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register team in mix", hoursLogged: 8, priority: "high" },
//     { number: 2, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register teamz in mix", hoursLogged: 2, priority: "low" },
//     { number: 3, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register teamzzz in mix", hoursLogged: 3, priority: "medium" },
// ]

function populateTickets(ticketsArr) {
    
    let tickets = [];
    ticketsArr.forEach((ticket) => {
        const { number, assignee, dueDate, summary, hoursLogged, priority, client, comments } = ticket;
        console.log("ticket m8: ", ticket, number, assignee, client); 
        tickets = [...tickets, new Ticket(number, assignee, dueDate, client, summary, hoursLogged, comments, priority)];
    });

    for (let i = 0; i < tickets.length; i++) {
        // console.log("Ticket info: ", tickets[i]);

        // Create HTML elements so we can inject them dynamically
        let ticketBody = document.querySelector(".ticket_body");
        let accordionBtn = document.createElement("button");
        let ticketTable = document.createElement("table");
        let ticketRow = document.createElement("tr");
        let ticketKey = document.createElement("th");
        let ticketSummary = document.createElement("th");
        let ticketAssignee = document.createElement("th");
        let ticketClient = document.createElement("th");
        let ticketStatus = document.createElement("th");
        let ticketHoursLogged = document.createElement("th");
        let ticketPriority = document.createElement("th");
        let ticketPanel = document.createElement("div");
        let ticketHeaders = [ticketKey, ticketSummary, ticketAssignee, ticketClient, ticketStatus, ticketHoursLogged, ticketPriority];

        // Set necessary classes
        accordionBtn.className = "accordion";
        ticketTable.className = "ticket_table";
        ticketPanel.className = "panel";

        // Build up the DOM hierarchy
        ticketHeaders.forEach(header => ticketRow.appendChild(header));
        ticketTable.appendChild(ticketRow);
        accordionBtn.appendChild(ticketTable);
        ticketBody.appendChild(accordionBtn);
        ticketBody.appendChild(ticketPanel);

        // Set up text content
        const { number, assignee, summary, hoursLogged, priority, status, client, comments } = tickets[i].getTicketInfo();
        ticketKey.textContent = number;
        ticketSummary.textContent = summary;
        ticketAssignee.textContent = assignee;
        ticketHoursLogged.textContent = hoursLogged;
        ticketPriority.textContent = priority;
        ticketClient.textContent = client; 
        ticketStatus.textContent = status;
        ticketPanel.textContent = comments;

    }

    addAccordionClick();

}

////////////////// Populate Accordion End//////////////////

/*

<div class="message_container" style="position: relative;width: 100%;height: auto;">
<div class="message" style="margin: 30px;">
<p id="message-user">Kevina</p>
<div style="background-color: #E3E3E3;padding: 0 5px;border: solid 1px black;width: 300px;" class="message-text"><p>Hi I'm Kevina. The VA.</p></div>
</div></div>
*/
function main() {
    addChatClick();
}

main();
let submit_button = document.getElementById('input-button');
let chat_window = document.getElementById('text_container');

async function fetch_start() {
    try {
        const urls = [
            `${window.origin}/tickets`,
            `${window.origin}/chat`
        ]

        const promises = await Promise.all(urls.map(async(url) => { let response = await fetch(url); return response.json() }));
        console.log("Promises: ", promises);
        console.log("Promise has been resolved!");

        let [tickets, json] = [...promises]

        console.log('json: ', json);

        update_chat(json.userText);
        populateTickets(JSON.parse(JSON.stringify(tickets))); 
        return
    } catch (error) {
        console.log("Seems like it didn't work out fam", error.message);
    }
}

async function fetch_continue(msg) {
    try {
        let response = await fetch(`${window.origin}/chat`, {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                "userText": msg
            })
        });
        if (!response.ok) {
            throw new Error("Network failed rip.")
        } else {
            let json = await response.json();
            console.log("This is the userText", json.userText)
            update_chat(json.userText)
        }
    } catch (error) {
        console.log("Seems like it didn't work out fam", error.message);
    }
}

function update_chat(msg, user = "InnoVAtor") {
    console.log("update chat msg: ", msg);
    let message_container = document.createElement('div');
    let message_user = document.createElement('p');
    let message_bubble = document.createElement('div');
    let message = document.createElement('p');

    message_container.className = "message";
    message_user.className = "message-user";
    message_bubble.className = "message-text";
    if (user == "InnoVAtor") {
        message_container.classList.add("message-va");
    }
    message.innerText = msg;
    message_user.innerText = user;

    message_container.appendChild(message_user);

    message_bubble.appendChild(message);
    message_container.appendChild(message_bubble);
    chat_window.appendChild(message_container);
}


submit_button.addEventListener('click', function(event) {
    event.preventDefault();
    let message_value = document.getElementById('fname').value;
    update_chat(message_value, "Me");
    fetch_continue(message_value);
    document.getElementById('fname').value = "";
});
fetch_start();

/*


<div class="message" style="margin: 30px;">
<p id="message-user">Kevina</p>
<div style="background-color: #E3E3E3;padding: 0 5px;border: solid 1px black;width: 300px;" class="message-text"><p>Hi I'm Kevina. The VA.</p></div>
</div></div>
*/