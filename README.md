# nginx ui    

![Docker Image CI](https://github.com/schenkd/nginx-ui/workflows/Docker%20Image%20CI/badge.svg)     

![Image of Nginx UI](https://i.ibb.co/XXcfsDp/Bildschirmfoto-2020-06-20-um-18-40-27.png)

![Image of Nginx UI](https://i.ibb.co/XXcfsDp/Bildschirmfoto-2020-06-20-um-18-40-27.png)

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

## UI

![Image of Nginx UI](https://i.ibb.co/qNgBRrt/Bildschirmfoto-2020-06-21-um-10-01-46.png)

With the menu item Main Config the Nginx specific configuration files
can be extracted and updated. These are dynamically read from the Nginx
directory. If a file has been added manually, it is immediately integrated
into the Nginx UI Main Config menu item.

![Image of Nginx UI](https://i.ibb.co/j85XKM6/Bildschirmfoto-2020-06-21-um-10-01-58.png)

Adding a domain opens an exclusive editing window for the configuration
file. This can be applied, deleted and enabled/disabled.
