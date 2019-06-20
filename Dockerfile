FROM debian:stretch-slim

RUN set -x \
        && apt-get update \
        && apt-get install -y --no-install-recommends --no-install-suggests \
                git \
                make \
        && pip install --upgrade pip \
        && cd /root \
        && git clone https://github.com/CM2Walki/scalexctl \
        && cd /root/scalexctl/scalexctl \
        && cd /root/scalexctl \
        && make init clean-build build \
        && rm -rf scalexctl \
        && apt-get clean autoclean \
        && apt-get autoremove -y \
        && rm -rf /var/lib/{apt,dpkg,cache,log}/

EXPOSE 20000

CMD [ "scalexctl", "start", "--attach"]
