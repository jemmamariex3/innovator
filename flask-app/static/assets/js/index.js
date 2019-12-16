//import { resolve } from "dns";

// With CSS loader, we can import the css in the main JS file, rather than the html file
//import "../css/styles.css";
//import Ticket from "./Ticket.js";
// import { configs } from './key';

// const token = require("../../dialog_proto/token_scripts/my-token.json");
// console.log("Hi, this is our key object: ", configs);
// console.log("Token json: ", token);

//////////////////// Accordion JS Start //////////////////
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
        }
    });
}
////////////////// Accordion JS End ////////////////////

class Ticket {
    constructor(number, assignee, dueDate, summary, hoursLogged, priority = "low", status = "open", startDate = new Date()) {
        this.number = number;
        this.assignee = assignee;
        this.dueDate = dueDate;
        this.summary = summary;
        this.hoursLogged = hoursLogged;
        this.priority = priority;
        this.status = status;
        this.startDate = startDate;
    }
}

////////////////// Populate Accordion Start //////////////////
let ticketsArr = [
    //why is this reversed.... & why are some slots undefined..
    (1, "High", "Register team in Mix", "12/19/2019", "DaLarm Han", 1),
    (1, "High", "Register team in Mix", "12/19/2019", "DaLarm Han", 2),
    (1, "High", "Register team in Mix", "12/19/2019", "DaLarm Han", 3)
]
let tickets = [];
ticketsArr.forEach((ticket) => tickets.push(new Ticket(ticket)));

for (var i = 0; i < tickets.length; i++) {
    console.log(tickets[i]);
    console.log(tickets[i].number);
}

//test #2
// let ticket2 = new Ticket(1,"DaLarm  Han","12/19/2019","Register team in Mix","High",1);
// console.log(ticket2.number);
////////////////// Populate Accordion End//////////////////

let submit_button = document.getElementById('input-button');
let chat_window = document.getElementById('message_container');

async function fetch_start() {
    try {
        let response = await fetch(`${window.origin}/startchat`);
        if (!response.ok) {
            throw new Error("Network response failed.");
        } else {
            let json = await response.json();
            update_chat(json.message);
            return
        }
    } catch (error) {
        console.log("Seems like it didn't work out fam", error.message);
    }
}

function update_chat(msg, user = "Kevina") {
    console.log(msg);
    let message_container = document.createElement('div');
    let message_user = document.createElement('p');
    let message_bubble = document.createElement('div');
    let message = document.createElement('p');

    message_container.className = "message";
    message_user.className = "message-user";
    message_bubble.className = "message-text";
    if (user == "Kevina") {
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
    document.getElementById('fname').value = "";
    fetch_start();
});

/*


<div class="message" style="margin: 30px;">
<p id="message-user">Kevina</p>
<div style="background-color: #E3E3E3;padding: 0 5px;border: solid 1px black;width: 300px;" class="message-text"><p>Hi I'm Kevina. The VA.</p></div>
</div></div>
*/