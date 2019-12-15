# Getting Started

	python3 -m venv env

	source env/bin/activate
	
	pip install -r requirements.txt

	python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ nuance_asr.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance_asr_resource.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance_asr_result.proto

	export CLIENT_ID="appID%3A<APP ID>"
	export CLIENT_SECRET="<CLIENT_SECRET>"
	export TOKEN="`curl -s -u "$CLIENT_ID:$CLIENT_SECRET" "https://auth.crt.nuance.com/oauth2/token" -d 'grant_type=client_credentials' -d 'scope=asr' | python -m json.tool |  python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])'`"

	python asr_client.py \
	--audioFile input.wav \
	--serverUrl asraas.beta.mix.nuance.com:443 \
	--secure --token $TOKEN \
	--dlmUrn "urn:nuance:mix/eng-USA/<TAG>/mix.asr"

# Troubleshooting
	
	kubectl --kubeconfig ~/.kube/config -n asraas-dev get pods

	# pick a pod
	KRYPTON_POD="krypton-b6686b666-69p8v"
	kubectl --kubeconfig ~/.kube/config -n asraas-dev logs -f $KRYPTON_POD krypton-container
