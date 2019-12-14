const token = require("./token_scripts/my-token.json");
const access_token = token.access_token;

const grpc = require('grpc');
const service_interface = require('./client_stubs/service-interface_grpc_pb');
const service_interface2 = require('./client_stubs/service-interface-messages_pb')

console.log("Token json: ", access_token);
console.log("service pb = ", service_interface);
console.log("service pb 2 = ", service_interface2);

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