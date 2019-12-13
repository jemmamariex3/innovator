class Ticket {
  constructor(number, assignee, dueDate, summary, priority = "low", status = "open", startDate = new Date()) {
      this.number = number;
      this.assignee = assignee;
      this.dueDate = dueDate;
      this.startDate = startDate;
      this.priority = priority;
      this.summary = summary;
      this.status = status;
  }
}

export default Ticket; 