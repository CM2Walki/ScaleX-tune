#!/bin/bash
ssh root@cm2.network << EOF
  docker start apmt
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune && git pull'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune/tune && python2.7 tunex.py stop'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune/tune && python2.7 tunex.py start'
EOF
