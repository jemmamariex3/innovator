const token = require("./token_scripts/my-token.json");
const access_token = token.access_token;

const grpc = require('grpc');
const runtime_interface = require('./client_stubs/runtime-interface-messages_pb');
const service_interface = require('./client_stubs/service-interface_grpc_pb'); // wtf is this
const chat_request = require('./client_stubs/service-interface-messages_pb');

// to start request == chat_request.StartRequest 

console.log("this is runtime stuff: ", runtime_interface.Selector);
console.log("what functios does service have: ", service_interface);
console.log("what functions does this have: ", chat_request);

function create_channel(args) {
    const access_token = args[1];
    var channel_credentials = grpc.Credentials.createSsl();
    var call_credentials = grpc.credentials.createFromMetadataGenerator((context, callback) => {
        metadata = new grpc.Metadata();
        metadata.set('Authorization', `Bearer ${access_token}`);
        console.log(metadata);
        callback(null, metadata);
    });
    channel_credentials = grpc.credentials.combineChannelCredentials(channel_credentials, call_credentials);
    console.log("niceee", channel_credentials);
    return channel_credentials;
}

function start_request(stub, model_ref, session_id, selector_dict = {}) {
    selector = runtime_interface.Selector(channel = selector_dict['channel'],
        library = selector_dict['library'],
        language = selector_dict['language']);
    start_payload = runtime_interface.StartRequestPayload(model_ref = model_ref);
    start_req = chat_request.StartRequest(session_id = session_id,
        selector = selector,
        payload = start_payload);
    console.log("Start Request: ", start_req);
    start_response, call = stub.Execute.with_call(start_req);
    console.log("Start Request Response: ", start_response);
    return start_response, call;
}

var first_channel = create_channgel(process.argv);
var stub =


    //   chat_request  === this will have all the Request shit.        
    //   hmMmMmmM i think this SHOULD have startRequest / executeRequest / blah blah
    //