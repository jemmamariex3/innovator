// With CSS loader, we can import the css in the main JS file, rather than the html file
import "../css/styles.css";
import { configs } from "./key";

const token = require("../../dialog_proto/token_scripts/my-token.json");

console.log("Hi, this is our key object: ", configs);
console.log("Token json: ", token);
