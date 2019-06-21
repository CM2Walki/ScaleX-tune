FROM debian:stretch-slim

RUN set -x \
        && apt-get update \
        && apt-get install -y --no-install-recommends --no-install-suggests \
                git \
                make \
                python \
                python-dev \
                python-pip \
                python-setuptools \
                python-wheel \
                build-essential \
                default-libmysqlclient-dev \
        && cd /root \
        && git clone https://github.com/CM2Walki/scalexctl \
        && cd /root/scalexctl \
        && pip install -r requirements.txt \
        && make init clean-build build \
        && rm -rf scalexctl \
        && apt-get remove --purge -y \
                git \
                make \
                python \
                python-dev \
                python-pip \
                python-setuptools \
                python-wheel \
                build-essential \
        && apt-get clean autoclean \
        && apt-get autoremove -y \
        && rm -rf /var/lib/{apt,dpkg,cache,log}/

EXPOSE 20000

ENTRYPOINT rm /tmp/scalexctl-daemon.pid > /dev/null 2>&1 \
                && scalexctl start --attach