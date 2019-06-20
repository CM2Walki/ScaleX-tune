FROM 2.7.16-alpine3.9

RUN set -x \
        && apk add --no-cache --virtual .build-deps \
                git \
                make \
        && git clone https://github.com/CM2Walki/scalexctl \
        && make init clean-build build \
        && rm -rf scalexctl \
        && apk del \
                git \
                make \
        && rm -rf scalexctl /var/cache/apk/*

EXPOSE 20000

CMD [ "scalexctl", "start", "--attach"]
