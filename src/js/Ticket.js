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

export default Ticket;