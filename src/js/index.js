// With CSS loader, we can import the css in the main JS file, rather than the html file
import "../css/styles.css";
import Ticket from "./Ticket.js";
// import { configs } from './key';

// const token = require("../../dialog_proto/token_scripts/my-token.json");
// console.log("Hi, this is our key object: ", configs);
// console.log("Token json: ", token);

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
const ticketsArr = [
  { number: 1, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register team in mix", hoursLogged: 8, priority: "high" }, 
  { number: 2, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register teamz in mix", hoursLogged: 2, priority: "low" }, 
  { number: 3, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register teamzzz in mix", hoursLogged: 3, priority: "medium" }, 
]
let tickets = [];
ticketsArr.forEach((ticket) => {
  const { number, assignee, dueDate, summary, hoursLogged, priority } = ticket; 
  tickets = [ ...tickets, new Ticket( number, assignee, dueDate, summary, hoursLogged, priority ) ]; 
});

for ( let i = 0; i < tickets.length; i++ ) {
  console.log("Ticket info: ", tickets[i]);
  
  // Create HTML elements so we can inject them dynamically
  let ticketBody = document.querySelector(".ticket_body"); 
  let accordionBtn = document.createElement("button"); 
  let ticketTable = document.createElement("table");
  let ticketRow = document.createElement("tr"); 
  let ticketKey = document.createElement("th"); 
  let ticketSummary = document.createElement("th"); 
  let ticketAssignee = document.createElement("th"); 
  let ticketStatus = document.createElement("th"); 
  let ticketHoursLogged = document.createElement("th"); 
  let ticketPriority = document.createElement("th"); 
  let ticketPanel = document.createElement("div"); 
  let ticketHeaders = [ticketKey, ticketSummary, ticketAssignee, ticketStatus, ticketHoursLogged, ticketPriority]; 

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
  // ticketKey.textContent = tickets[i].
  const { number, assignee, summary, hoursLogged, priority, status } = tickets[i].getTicketInfo(); 
  ticketKey.textContent = number; 
  ticketSummary.textContent = summary; 
  ticketAssignee.textContent = assignee; 
  ticketHoursLogged.textContent = hoursLogged; 
  ticketPriority.textContent = priority; 
  ticketStatus.textContent = status; 
  ticketPanel.textContent = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequuntur fugiat quod architecto libero tempora voluptates quo, eius sequi? Repudiandae, ea"; 
  
  console.log("Ticket body el: ", ticketHeaders); 


}

////////////////// Populate Accordion End//////////////////

/*

<div class="message_container" style="position: relative;width: 100%;height: auto;">
<div class="message" style="margin: 30px;">
<p id="message-user">Kevina</p>
<div style="background-color: #E3E3E3;padding: 0 5px;border: solid 1px black;width: 300px;" class="message-text"><p>Hi I'm Kevina. The VA.</p></div>
</div></div>
*/

addAccordionClick(); 