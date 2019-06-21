FROM debian:stretch-slim

RUN set -x \
        && apt-get update \
        # Install all requirements for pyinstaller and the ScaleX-Daemon
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
        # Clone repository
        && git clone https://github.com/CM2Walki/scalexctl \
        && cd /root/scalexctl \
        # Install python modules
        && pip install -r requirements.txt \
        # Make clean build (also moves build to /usr/bin)
        && make init clean-build build \
        # Tidy up; Remove all python modules, remove repo & uninstall packages + clean up
        && pip uninstall -r requirements.txt -y \
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
                default-libmysqlclient-dev \
        && apt-get clean autoclean \
        && apt-get autoremove -y \
        && rm -rf /var/lib/{apt,dpkg,cache,log}/

EXPOSE 20000

# Delete old .pid file of the daemon if it was created
# Start and attach to the daemon
ENTRYPOINT rm -f /tmp/scalexctl-daemon.pid \
                && scalexctl start --attach