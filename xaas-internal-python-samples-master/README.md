# Getting Started

## Create a token

A token is required to access the services. 

Mix offers the ability to generate an oauth2 client with the user's App ID. The secret is presented to the user and used thereafter. (WIP)

To perform this operational during development/testing:

Get the Hydra Admin URL:

	kubectl --kubeconfig ~/.kube/config get pod -n global-auth-dev -o wide | grep hydra-dev

	export HYDRA_ADMIN=http://10.58.194.251:4445

Describe the Client ID and Name to create (simulating an App ID):

	export CLIENT_ID="appID:NMDPTRIAL_nirvana_tikku_nuance_com_20190919T190532"
	export CLIENT_NAME="Sandbox-AzureEastUS-nirvana.tikku@nuance.com"

Execute the call against the Hydra Admin API, providing all service scopes and the properties defined below

	docker run --rm oryd/hydra clients create -c "" -g client_credentials --id "$CLIENT_ID" -n "$CLIENT_NAME" -a asr,nlu,dialog,tts --endpoint $HYDRA_ADMIN

Observe the response and store the secret:

	OAuth 2.0 Client ID: appID:NMDPTRIAL_nirvana_tikku_nuance_com_20190919T190532
	OAuth 2.0 Client Secret: <<STORE THIS>>

List the clients:

	docker run --rm oryd/hydra clients list --endpoint $HYDRA_ADMIN

## Execute against the services

ASR, TTS and NLU are currently available.

TTS does not offer Mix specific customization artifacts, and therefore centers around calling text to speech as a service directly.

ASR does offer Mix specific customization artifacts, by way of DLM, and exposes a URN to be referenced. 

NLU executes Mix authored artifacts, the NLU model, exposed by a URN which points to specific versions in an application config.

Navigate to the sub directories and see the README's for more info.
