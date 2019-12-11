#!/bin/bash

CLIENT_ID="appID%3A3ANMDPTRIAL_dalarm_han_nuance_com_20191202T192457940935"
SECRET="mJ7iKz81mK724Ufic73d_0x81h9_B_nNhZKlwVSqT5k"
MY_TOKEN="`curl -s -u "$CLIENT_ID:$SECRET" "https://auth.crt.nuance.com/oauth2/token" \
-d 'grant_type=client_credentials' -d 'scope=dlg' \
| python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])'`"
