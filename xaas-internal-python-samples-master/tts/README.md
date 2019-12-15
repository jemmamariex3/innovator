# Getting Started

	python3 -m venv env

	source env/bin/activate
	
	pip install -r requirements.txt

	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. nuance_tts.proto

	export CLIENT_ID="appID%3A<APP ID>"
	export CLIENT_SECRET="<CLIENT_SECRET>"
	export TOKEN="`curl -s -u "$CLIENT_ID:$CLIENT_SECRET" "https://auth.crt.nuance.com/oauth2/token" -d 'grant_type=client_credentials' -d 'scope=tts' | python -m json.tool |  python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])'`"

	python tts_client.py \
	--serverUrl ttsaas.beta.mix.nuance.com:443 \
	--secure --token $TOKEN \
	-f flow.py \
	--saveAudio

	brew install sox

	play -c1 -b16 -esigned -traw -r22050 flow.py_i1_s1.pcm

# Troubleshooting
	
	kubectl --kubeconfig ~/.kube/config -n ttsaas-dev get pods

	# pick a pod
	NVC_POD="ttsaas-dev-nvc-57999d4dd4-mdfhw"
	kubectl --kubeconfig ~/.kube/config -n ttsaas-dev logs -f $NVC_POD nvc
