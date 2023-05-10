FROM python:3.7-alpine

ADD requirements.txt .

RUN apk add curl python3-dev build-base linux-headers pcre-dev && pip install --no-cache-dir -r requirements.txt

RUN cd /tmp/ \
    && curl -sSL -O https://download.docker.com/linux/static/stable/x86_64/docker-17.06.2-ce.tgz \
    && tar zxf docker-17.06.2-ce.tgz \
    && mkdir -p /usr/local/bin \
    && mv ./docker/docker /usr/local/bin \
    && chmod +x /usr/local/bin/docker \
    && rm -rf /tmp/*

# adding application files
ADD . /webapp

# configure path /webapp to HOME-dir
ENV HOME /webapp
WORKDIR /webapp
EXPOSE 8080

ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:8080", "--wsgi-file", "wsgi.py", "--callable", "app", "--processes", "1", "--threads", "8"]