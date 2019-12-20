#!/bin/bash

CLIENT_ID="appID%3ANMDPTRIAL_dalarm_han_nuance_com_20191202T192457940935"
SECRET="zvqtKbRmXMVH9Di9EwXJpFOHZfDFQufmR6XcvXu4IXk"
curl -s -u "$CLIENT_ID:$SECRET" "https://auth.crt.nuance.com/oauth2/token" \
-d 'grant_type=client_credentials' -d 'scope=dlg' \
| python -c 'import os, sys, json; print(json.load(sys.stdin)["access_token"])' \
> my-token.txt