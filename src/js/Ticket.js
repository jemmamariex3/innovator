class Ticket {
  constructor(number, assignee, dueDate, summary, hoursLogged, comment, priority = "low", status = "open", startDate = new Date()) {
      this.number = number;
      this.assignee = assignee;
      this.dueDate = dueDate;
      this.summary = summary;
      this.hoursLogged = hoursLogged;
      this.comment = comment;
      this.priority = priority;
      this.status = status;
      this.startDate = startDate;
  }

  getTicketInfo() {
    const { ...params } = this; 
    
    return params; 
  }
}

export default Ticket;