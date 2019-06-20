FROM python:2-alpine

RUN set -x \
        && cd /root \
        && apk add --no-cache --virtual .build-deps \
                git \
                make \
                zlib-dev \
                musl-dev \
                libc-dev \
                gcc \
        && pip install --upgrade pip
        && git clone https://github.com/CM2Walki/scalexctl \
        && cd /root/scalexctl \
        && make init clean-build build \
        && rm -rf scalexctl \
        && apk del \
                git \
                make \
                zlib-dev \
                musl-dev \
                libc-dev \
                gcc \
        && rm -rf scalexctl /var/cache/apk/*

EXPOSE 20000

CMD [ "scalexctl", "start", "--attach"]
