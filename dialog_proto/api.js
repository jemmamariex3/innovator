var grpc = require('grpc');
var GoogleAuth = require('google-auth-library');

function create_channel(args) {
    args = process.argv;
    var channel_credentials = grpc.Credentials.createSsl(root_certs);
    var call_credentials = "omg how do?";
    channel_credentials = grpc.credentials.combineChannelCredentials(channel_credentials, call_credentials);
    return channel_credentials;
}