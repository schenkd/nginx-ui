FROM ubuntu:18.04 AS base

# apt installs
# For backend
RUN apt-get update && apt-get install -y python3.7 python3-pip build-essential git curl sudo net-tools nginx vim

# For frontend
WORKDIR /root
ENV NVM_DIR /root/.nvm
ARG version_nvm=0.37.2
ARG version_node=17.3.1
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v$version_nvm/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $version_node \
    && nvm use $version_node
ENV PATH $NVM_DIR/versions/node/v$version_node/bin:$PATH

FROM base AS nginx-ui
RUN mkdir /root/nginx-ui
ADD . /root/nginx-ui
# For backend
RUN pip3 install -r /root/nginx-ui/app/backend/requirements

# For frontend
WORKDIR /root/nginx-ui/app/frontend
RUN npm install

# For nginx
ADD wish-nginx-ui.conf /etc/nginx/conf.d/
RUN service nginx reload

WORKDIR /root/nginx-ui
CMD ["/bin/bash", "-c", "echo Feel free to ctrl-c! Container will stick around. && while true ; do sleep 3600; done"]