# nginx ui

![Docker Image CI](https://github.com/schenkd/nginx-ui/workflows/Docker%20Image%20CI/badge.svg)

![Image of Nginx UI](https://i.ibb.co/XXcfsDp/Bildschirmfoto-2020-06-20-um-18-40-27.png)

Table of Contents

- [nginx ui](#nginx-ui)
  - [Introduction](#introduction)
  - [Setup](#setup)
    - [Example](#example)
    - [Docker](#docker)
  - [UI](#ui)
  - [Authentication](#authentication)
    - [Configure the auth file](#configure-the-auth-file)
    - [Configure nginx](#configure-nginx)

## Introduction

We use nginx in our company lab environment. It often happens that my
colleagues have developed an application that is now deployed in our Stage
or Prod environment. To make this application accessible nginx has to be
adapted. Most of the time my colleagues don't have the permission to access
the server and change the configuration files and since I don't feel like
doing this for everyone anymore I thought a UI could help us all. If you
feel the same way I wish you a lot of fun with the application and I am
looking forward to your feedback, change requests or even a star.

## Setup

Containerization is now state of the art and therefore the application is
delivered in a container.

### Example

- `-d` run as deamon in background
- `--restart=always` restart on crash or server reboot
- `--name nginxui` give the container a name
- `-v /etc/nginx:/etc/nginx` map the hosts nginx directory into the container
- `-p 8080:8080` map host port 8080 to docker container port 8080

```bash
docker run -d --restart=always --name nginxui -v /etc/nginx:/etc/nginx -p 8080:8080 schenkd/nginx-ui:latest
```

### Docker

Repository @ [DockerHub](https://hub.docker.com/r/schenkd/nginx-ui)

Docker Compose excerpt

```yaml
# Docker Compose excerpt
services:
  nginx-ui:
    image: schenkd/nginx-ui:latest
    ports:
      - 8080:8080
    volumes:
      - nginx:/etc/nginx
```

## UI

![Image of Nginx UI](https://i.ibb.co/qNgBRrt/Bildschirmfoto-2020-06-21-um-10-01-46.png)

With the menu item Main Config the Nginx specific configuration files
can be extracted and updated. These are dynamically read from the Nginx
directory. If a file has been added manually, it is immediately integrated
into the Nginx UI Main Config menu item.

![Image of Nginx UI](https://i.ibb.co/j85XKM6/Bildschirmfoto-2020-06-21-um-10-01-58.png)

Adding a domain opens an exclusive editing window for the configuration
file. This can be applied, deleted and enabled/disabled.

## Authentication

[BasicAuth with nginx](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

In general, this app does not come with authentication. However, it is easy to setup basic auth to restrict unwanted access.
Here is how this can be done when using nginx.

### Configure the auth file

1. Verify that `apache2-utils` (Debian, Ubuntu) or `httpd-tools` (RHEL/CentOS/Oracle Linux) is installed
2. Run the htpasswd utility to create a new user and set a passwort.
    - Make sure, that the directory exists
    - Remove the `-c` flag, if you have created a user before, since it creates the inital user/passwort file
    - `sudo htpasswd -c /etc/apache2/.htpasswd user1`

### Configure nginx

The following example adds basic auth to our nginxui app running in a docker container with a mapped port 8080.
In this case, it will be accessible via nginx.mydomain.com

```none
server {
    server_name nginx.mydomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080/;
    }

    auth_basic "nginxui secured";
    auth_basic_user_file /etc/apache2/.htpasswd;

    # [...] ommited ssl configuration
}
```

1. Add above nginx conf to your `/etc/nginx/my.conf` file
2. Run `nginx -t` to make sure, that your config is valid
3. Run `systemctl restart nginx` (or equivalent) to restart your nginx and apply the new settings
4. Your nginx ui is now accessible at nginx.mydomain.com and will correctly prompt for basic auth
