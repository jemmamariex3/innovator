function create_channel(args) {
    args = process.argv;
    var channel_credentials = grpc.Credentials.createSsl();
    var call_credentials = grpc.credentials.createFromMetadataGenerator((context, callback) => {
        metadata = new grpc.Metadata();
        metadata.set('Authorization', `Bearer ${token}`);
        console.log(metadata);
        callback(null, metadata);
    });
    channel_credentials = grpc.credentials.combineChannelCredentials(channel_credentials, call_credentials);
    return channel_credentials;
}