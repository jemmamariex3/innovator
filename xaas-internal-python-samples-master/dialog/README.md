# Getting Started

	python3 -m venv env

	source env/bin/activate
	
	pip install -r requirements.txt

	python -m grpc_tools.protoc --proto_path=./ --python_out=./ google/api/http.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ google/api/annotations.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/dialog/v1beta1/runtime-interface-messages.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/dialog/v1beta1/service-interface-messages.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ nuance/dialog/v1beta1/service-interface.proto

	export CLIENT_ID="appID%3A<APP ID>"
	export CLIENT_SECRET="<CLIENT_SECRET>"
	export TOKEN="`curl -s -u "$CLIENT_ID:$CLIENT_SECRET" "https://auth.crt.nuance.com/oauth2/token" -d 'grant_type=client_credentials' -d 'scope=dlg' | python -m json.tool |  python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])'`"

	python dlg_client.py \
	--serverUrl dlgaas.beta.mix.nuance.com:443 \
	--secure --token $TOKEN \
	--modelUrn "urn:nuance:mix/eng-USA/<TAG>/mix.dialog" \
	--textInput "hello world"

# Parameters and Troubleshooting

	replace modelUrn with your URN
	serverUrl must contain hostname:port
	provide nmaid if required else keep it ''
