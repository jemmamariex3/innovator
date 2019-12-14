const token = require("./token_scripts/my-token.json");
const access_token = token.access_token;

const grpc = require('grpc');
const service_interface = require('./client_stubs/service-interface_grpc_pb'); // wtf is this
const chat_request = require('./client_stubs/service-interface-messages_pb');

// to start request == chat_request.StartRequest 

console.log("Token json: ", access_token);
console.log("what functions does this have: ", chat_request);

function create_channel(args) {
    args = process.argv;
    var channel_credentials = grpc.Credentials.createSsl();
    var call_credentials = grpc.credentials.createFromMetadataGenerator((context, callback) => {
        metadata = new grpc.Metadata();
        metadata.set('Authorization', `Bearer ${access_token}`);
        console.log(metadata);
        callback(null, metadata);
    });
    channel_credentials = grpc.credentials.combineChannelCredentials(channel_credentials, call_credentials);
    return channel_credentials;
}

function start_request(stub, model_ref, session_id, selector_dict = {}) {

}


//   chat_request  === this will have all the Request shit.        
//   hmMmMmmM i think this SHOULD have startRequest / executeRequest / blah blah
//