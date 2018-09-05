#!/bin/bash
ssh root@cm2.network << EOF
  docker start apmt
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune && git pull'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune && pip install -r requirements.txt'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune/tune && ./tunex.py restart'
EOF