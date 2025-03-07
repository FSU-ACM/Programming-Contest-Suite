---
layout: default
title: Docker Image
grand_parent: Deployment
parent: Docker
nav_order: 1
---

# Docker Image

The project's `Dockerfile` is designed to build both the development and production versions of the project's Docker Image. 

## Build Image

```bash
# Programming-Contet-Suite/

docker build . -t <image_name> --build-arg="REQUIREMENTS=requirements.txt"
```

`Dockerfile` Argument | Default | Description
---|---|---
REQUIREMENTS | requirements.txt | Path to the manifest file to use during image creation.

## Run Image

The `Dockerfile` specifies an image capable of running the Django web app with Celery. The parameters passed to the image's start script `start.sh` determine the container's behavior.

```bash
docker run <image_name> /docker/start.sh <PROCESS_TYPE> <MODE>
```

`PROCESS_TYPE` | Default | Usage
---|---|---
server | Yes | Gunicorn server bound to the Django app
worker | No | Celery Worker
beat | No | Celery Beat
flower | No | Celery Flower

`MODE` | Default | Usage
---|---|---
production | Yes | Option specified by `PROCESS_TYPE` uses production ready settings/flags.
debug | No | Option specified by `PROCESS_TYPE` uses debug/development settings/flags.

### Default Superuser Account
user: `contestadmin`  
pass: `seminoles1!`

A default Django superuser account is created when the container connects to an empty database. The default password can be replaced using Django administration. A link to the Django administration interface is located in the user's navigation menu, when logged in using this account.
