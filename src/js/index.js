// With CSS loader, we can import the css in the main JS file, rather than the html file
import "../css/styles.css";
import { configs } from './key';

console.log("Hi, this is our key object: ", configs);
console.log('Hi')
    // With CSS loader, we can import the css in the main JS file, rather than the html file
import "../css/styles.css";
import { configs } from './key';

console.log("Hi, this is our key object: ", configs);

/*Most likely going to some other js file and we can import ?_? */

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

class User {
    constructor(name, assigned = []) {
        name = this.name;
    }
}