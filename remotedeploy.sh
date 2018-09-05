#!/bin/bash
# Add the ScaleX module to an existing container
# Creates a ScaleX container if it doesn't exist already
if [ -z $1 ] || [ -z $2 ] || [ -z $3 ]; then
  printf 'Not enough arguments provided!\n\n'
  printf 'Usage: ./remotedeploy.sh REMOTE SCALEXPORT SCALEXCONTAINERNAME\n\n'
  printf 'Example: ./remotedeploy.sh root@example.org 8080 ScaleX\n'
  exit 1;
fi
REMOTE=$1
SCALEXPORT=$2
SCALEXCONTAINERNAME=$3
ssh $REMOTE << EOF
  if ! docker start '$SCALEXCONTAINERNAME'; then docker run -d -p '$SCALEXPORT':8080 --name='$SCALEXCONTAINERNAME' walki/apmt; fi
  docker exec '$SCALEXCONTAINERNAME' bash -c 'if cd /usr/src/ScaleX-tune; then git fetch --all && git reset --hard origin/master; else cd /usr/src/ && git clone https://github.com/CM2Walki/ScaleX-tune; fi'
  docker exec '$SCALEXCONTAINERNAME' bash -c 'cd /usr/src/ScaleX-tune && make init clean-build build'
  docker exec '$SCALEXCONTAINERNAME' bash -c 'cd /usr/src/ScaleX-tune/tunex && tunex restart'
  printf 'Deployment script done.\n'
EOF