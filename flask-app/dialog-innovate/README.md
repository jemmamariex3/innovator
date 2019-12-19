# Getting Started (Mac)

## Install Virtual Environment & Dependencies

	python3 -m venv env

	source env/bin/activate
	
	pip install -r requirements.txt

	python -m grpc_tools.protoc --proto_path=./ --python_out=./ google/api/http.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ google/api/annotations.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/dialog/v1beta1/runtime-interface-messages.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/dialog/v1beta1/service-interface-messages.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ nuance/dialog/v1beta1/service-interface.proto

## Auth Token

	export CLIENT_ID="appID%3AREPLACEME"
	export CLIENT_SECRET="REPLACEME"
	export TOKEN="`curl -s -u "$CLIENT_ID:$CLIENT_SECRET" "https://auth.crt.nuance.com/oauth2/token" -d 'grant_type=client_credentials' -d 'scope=dlg' | python -m json.tool |  python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])'`"

## Run the Client

	python dlg_client.py \
	--serverUrl dlgaas.beta.mix.nuance.com:443 \
	--secure --token $TOKEN \
	--modelUrn "urn:nuance:mix/eng-USA/<TAG>/mix.dialog"

## Usage
	
	usage: dlg_client.py [-options]
	options:
	  -h, --help                   Show this help message and exit
	  -s [url], --serverUrl [url]  Dialog server URL, default=localhost:8080
	  --modelUrn [MODELURN]        Dialog App URN, e.g. urn:nuance:mix/eng-USA/A2_C16/mix.dialog
	  --secure                     Connect to the server using a secure gRPC channel.
	  --rootCerts [file]           Root certificates when using secure channel.
	  --privateKey [file]          Certificate private key when using secure channel.
	  --certChain [file]           Certificate chain when using secure channel.
	  --debug                      Show debugging logs.

# Parameters and Troubleshooting

	replace modelUrn with your URN
	serverUrl must contain hostname:port
	provide nmaid if required else keep it ''


# Changelog

Dec 15, 2019

* Removed textInput
* Added --debug flag
* Added data node access support
* Updated to include DataClass for data access nodes
* Updated logic for handling prompts (concat string)

