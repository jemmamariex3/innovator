// With CSS loader, we can import the css in the main JS file, rather than the html file
import "../css/styles.css";
import Ticket from "./Ticket.js";
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

////////////////// Populate Accordion Start //////////////////
let ticketsArr = [
    //why is this reversed.... & why are some slots undefined..
    (1,"High","Register team in Mix","12/19/2019","DaLarm Han",1),
    (1,"High","Register team in Mix","12/19/2019","DaLarm Han",2),
    (1,"High","Register team in Mix","12/19/2019","DaLarm Han",3)
]
let tickets = [];
ticketsArr.forEach((ticket) => tickets.push(new Ticket(ticket)));

for(var i = 0; i < tickets.length;i++){
    console.log(tickets[i]);
    console.log(tickets[i].number);
}

//test #2
// let ticket2 = new Ticket(1,"DaLarm  Han","12/19/2019","Register team in Mix","High",1);
// console.log(ticket2.number);
////////////////// Populate Accordion End//////////////////
