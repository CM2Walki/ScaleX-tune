FROM python:2-alpine

RUN set -x \
        && cd /root \
        && apk --update --no-cache --virtual .build-deps add \
                git \
                make \
                zlib-dev \
                musl-dev \
                libc-dev \
                gcc \
                python2-tkinter \
        && pip install --upgrade pip \
        && ln -s /lib/libc.musl-x86_64.so.1 ldd \
        && ln -s /lib /lib64 \
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
                python2-tkinter \
        && rm -rf scalexctl /var/cache/apk/*

EXPOSE 20000

CMD [ "scalexctl", "start", "--attach"]
