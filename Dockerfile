FROM debian:stretch-slim

RUN set -x \
        && apt-get update \
        && apt-get install -y --no-install-recommends --no-install-suggests \
                git \
                make \
                python2.7 \
                python-pip \
                python-setuptools \
                python-dev \
                python-ctypes \
                python-all-dev \
                libevent-dev \
        && pip install --upgrade \
                pip \
                wheel \
                pyinstaller \
                greenlet \
                gevent \
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
