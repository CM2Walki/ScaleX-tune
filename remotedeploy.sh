#!/bin/bash
ssh root@cm2.network << EOF
  if ! docker start apmt; then docker run -d -p 8080:8080 --name=apmt walki/apmt; fi
  docker exec apmt bash -c 'if cd /usr/src/ScaleX-tune; then git fetch --all && git reset --hard origin/master; else cd /usr/src/ && git clone https://github.com/CM2Walki/ScaleX-tune; fi'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune && make init clean-build build'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune/tunex && tunex restart'
  echo 'Deployment script done.'
EOF