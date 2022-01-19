FROM ubuntu:18.04 AS base

# apt installs
# For backend
RUN apt-get update && apt-get install -y python3.7 python3-pip python3.7-dev build-essential git curl sudo net-tools nginx vim
RUN apt-get install -y dnsutils iputils-ping
RUN apt-get install -y python
ARG version_virtualenv=20.4.0
RUN pip3 install virtualenv==$version_virtualenv



FROM base AS app
RUN useradd --create-home app
# Put the app user from the base image in the sudo group for convenience
RUN usermod -a -G sudo app
# passwordless sudo
RUN sed -i '/^%sudo/c\%sudo ALL=(ALL:ALL) NOPASSWD:ALL' /etc/sudoers



FROM app AS fixuid
USER root
RUN curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.3/fixuid-0.3-linux-amd64.tar.gz | tar xzv -C /usr/bin
RUN chown root:root /usr/bin/fixuid && \
    chmod 4755 /usr/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    chown root:root /etc/fixuid && \
    printf "user: app\ngroup: app\npaths:\n  - /\n  - /home/app\n" > /etc/fixuid/config.yml \
USER app
ENTRYPOINT ["/usr/bin/fixuid"]

FROM fixuid AS frontend
USER app
# For frontend
WORKDIR /home/app
ENV NVM_DIR /home/app/.nvm
ARG version_nvm=0.37.2
ARG version_node=16.13.2
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v$version_nvm/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $version_node \
    && nvm use $version_node
ENV PATH $NVM_DIR/versions/node/v$version_node/bin:$PATH
RUN npm install -g @vue/cli

FROM frontend AS backend
USER app
RUN mkdir /home/app/virtualenv
RUN virtualenv -p /usr/bin/python3.7 --no-download /home/app/virtualenv

FROM backend AS nginx-ui
USER app
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /home/app
#ADD . /root/nginx-ui
# For backend
COPY ./app/backend/requirements /home/app/nginx-ui/app/backend/requirements
RUN /home/app/virtualenv/bin/pip install --exists-action w -r /home/app/nginx-ui/app/backend/requirements
ENV PATH /home/app/virtualenv/bin:$PATH
ENV VIRTUAL_ENV=/home/app/virtualenv
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONPATH /home/app/nginx-ui


WORKDIR /home/app
RUN git clone https://github.com/Conan-shen/marlon-tools.git

# For frontend
#WORKDIR /root/nginx-ui/app/frontend
#RUN npm install

# For nginx
#USER root
#ADD wish-nginx-ui.conf /etc/nginx/conf.d/
#RUN sudo service nginx start

CMD ["/bin/bash", "-c", "echo Feel free to ctrl-c! Container will stick around. && while true ; do sleep 3600; done"]