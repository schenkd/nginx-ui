FROM python:3.7-alpine

ADD requirements.txt .

RUN apk add python3-dev build-base linux-headers pcre-dev libffi-dev && pip install --no-cache-dir -r requirements.txt

# adding application files
ADD . /webapp

# configure path /webapp to HOME-dir
ENV HOME /webapp
WORKDIR /webapp

ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:8080", "--file", "wsgi.py", "--callable", "app", "--uid", "1000", "--master"]