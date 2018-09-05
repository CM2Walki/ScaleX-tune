#!/bin/bash
ssh root@cm2.network << EOF
  docker start apmt
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune && git fetch --all'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune && git reset --hard origin/master'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune && pip install -r requirements.txt'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune/tunex && chmod +x tunex.py'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune/tunex && pyinstaller --onefile tunex.py'
  docker exec apmt bash -c 'mv /usr/src/ScaleX-tune/tunex/dist/tunex /usr/bin/tunex'
  docker exec apmt bash -c 'cd /usr/src/ScaleX-tune/tunex && tunex restart'
  echo 'Deployment script done.'
EOF