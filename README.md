# nginx ui

![Image of Nginx UI](https://i.ibb.co/sj8pwCQ/Bildschirmfoto-2020-06-20-um-18-40-27.png)

We use nginx in our company lab environment. It often happens that my
colleagues have developed an application that is now deployed in our Stage
or Prod environment. To make this application accessible nginx has to be
adapted. Most of the time my colleagues don't have the permission to access
the server and change the configuration files and since I don't feel like
doing this for everyone anymore I thought a UI could help us all. If you
feel the same way I wish you a lot of fun with the application and I am
looking forward to your feedback, change requests or even a star.

## setup

Containerization is now state of the art and therefore the application is
delivered in a container.

### docker

Repository @ [DockerHub](https://hub.docker.com/r/schenkd/nginx-ui)

```yaml
services:
  nginx-ui:
    image: schenkd/nginx-ui:latest
    ports:
      - 8080:8080
    volumes:
      - nginx:/etc/nginx
```
