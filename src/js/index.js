// With CSS loader, we can import the css in the main JS file, rather than the html file
import "../css/styles.css";
import Ticket from "./Ticket.js";
// import { configs } from './key';

// const token = require("../../dialog_proto/token_scripts/my-token.json");
// console.log("Hi, this is our key object: ", configs);
// console.log("Token json: ", token);

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
// Global Vars
let ticketBody, accordionBtn, ticketTable, ticketRow, ticketKey, ticketSummary, ticketAssignee, ticketStatus, ticketHoursLogged, ticketPriority, ticketPanel, ticketHeaders;
let innerTable, innerRow, userHeader, commentHeader, userSection, commentSection, innerHeaders;

const ticketsArr = [
  { number: 1, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register team in mix", hoursLogged: 8, comment:"testing", priority: "high" }, 
  { number: 2, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register teamz in mix", hoursLogged: 2, comment:"testing", priority: "low" }, 
  { number: 3, assignee: "DaLarm Han", dueDate: "12/19/2019", summary: "Register teamzzz in mix", hoursLogged: 3, comment:"testing", priority: "medium" }, 
]
let tickets = [];
ticketsArr.forEach((ticket) => {
  const { number, assignee, dueDate, summary, hoursLogged, comment, priority } = ticket; 
  tickets = [ ...tickets, new Ticket( number, assignee, dueDate, summary, hoursLogged, comment, priority ) ]; 
});

for ( let i = 0; i < tickets.length; i++ ) {
  console.log("Ticket info: ", tickets[i]);
  
  // Create HTML elements so we can inject them dynamically
  ticketBody = document.querySelector(".ticket_body"); 
  accordionBtn = document.createElement("button"); 
  ticketTable = document.createElement("table");
  ticketRow = document.createElement("tr"); 
  ticketKey = document.createElement("th"); 
  ticketSummary = document.createElement("th"); 
  ticketAssignee = document.createElement("th"); 
  ticketStatus = document.createElement("th"); 
  ticketHoursLogged = document.createElement("th"); 
  ticketPriority = document.createElement("th"); 
  ticketPanel = document.createElement("div"); 
  ticketHeaders = [ticketKey, ticketSummary, ticketAssignee, ticketStatus, ticketHoursLogged, ticketPriority];
  
  innerTable = document.createElement("table");
  innerRow = document.createElement("tr"); 
  userHeader = document.createElement("th");
  commentHeader = document.createElement("th");
  userSection = document.createElement("td");
  commentSection = document.createElement("td");
  innerHeaders = [userHeader, commentHeader];

  // Set necessary classes
  accordionBtn.className = "accordion"; 
  ticketTable.className = "ticket_table"; 
  ticketPanel.className = "panel"; 
  innerTable.className = "inner_table";

  // Build up the DOM hierarchy
  ticketHeaders.forEach(header => ticketRow.appendChild(header));
  ticketTable.appendChild(ticketRow); 
  accordionBtn.appendChild(ticketTable); 
  ticketBody.appendChild(accordionBtn);
  ticketBody.appendChild(ticketPanel); 

  innerHeaders.forEach(innerHeader => innerRow.appendChild(innerHeader));
  innerTable.appendChild(innerRow); 
  innerTable.appendChild(userSection); 
  innerTable.appendChild(commentSection);
  ticketPanel.appendChild(innerTable);


  // Set up text content
  const { number, assignee, summary, hoursLogged, comment, priority, status } = tickets[i].getTicketInfo(); 
  ticketKey.textContent = number; 
  ticketSummary.textContent = summary; 
  ticketAssignee.textContent = assignee; 
  ticketHoursLogged.textContent = hoursLogged; 
  ticketPriority.textContent = priority; 
  ticketStatus.textContent = status; 
  userHeader.textContent = "User";
  commentHeader.textContent = "Comment";
  userSection.textContent = assignee;
  commentSection.textContent = comment;
  console.log("Ticket body el: ", ticketHeaders); 

}

////////////////// Populate Accordion End //////////////////

/*

<div class="message_container" style="position: relative;width: 100%;height: auto;">
<div class="message" style="margin: 30px;">
<p id="message-user">Kevina</p>
<div style="background-color: #E3E3E3;padding: 0 5px;border: solid 1px black;width: 300px;" class="message-text"><p>Hi I'm Kevina. The VA.</p></div>
</div></div>
*/
function main() {
  addAccordionClick(); 
  addChatClick(); 
}

main(); 