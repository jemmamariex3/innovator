# Getting Started

	python3 -m venv env

	source env/bin/activate
	
	pip install -r requirements.txt

	python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ nuance/nlu/v1beta1/runtime.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/nlu/v1beta1/result.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/nlu/v1beta1/interpretation-common.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/nlu/v1beta1/single-intent-interpretation.proto
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ nuance/nlu/v1beta1/multi-intent-interpretation.proto

	export CLIENT_ID="appID%3A<APP ID>"
	export CLIENT_SECRET="<CLIENT_SECRET>"
	export TOKEN="`curl -s -u "$CLIENT_ID:$CLIENT_SECRET" "https://auth.crt.nuance.com/oauth2/token" -d 'grant_type=client_credentials' -d 'scope=nlu' | python -m json.tool |  python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])'`"

	python nlu_client.py \
	--serverUrl nluaas.beta.mix.nuance.com:443 \
	--secure --token $TOKEN \
	--modelUrn "urn:nuance:mix/eng-USA/<TAG>/mix.nlu" \
	--textInput "Hello world"

# Troubleshooting
	
	kubectl --kubeconfig ~/.kube/config -n nluaas-dev get pods -o wide

	# pick a pod
	NLE_POD="nlu-api-server-845f64f844-6zq7r"
	kubectl --kubeconfig ~/.kube/config -n nluaas-dev logs -f $NLE_POD
