---
layout: default
title: Deployment
nav_order: 3
has_children: true
---

# Deployment

There are many ways to [deploy Django](https://docs.djangoproject.com/en/4.2/howto/deployment/). The articles in this section cover configuring the PCS, general deployment guidelines, and deploying both with and without Docker.

{: .important-title }
> Docker
>
> The project has been extenively tested with and includes files for deploying using [Docker](https://www.docker.com/). Please reference the project's [Docker documentation]({{ site.url }}/deployment/docker/) for usage information.

## Support Services

The project settings file[^1] and Flower settings file[^2] specify the use of several support services which run alongside the Django application server. Links to relevant documentation are available in the navigation menu.

- **Celery** <small>(Beat | Flower | Worker)</small>  
    Schedules, monitors, and performs asynchronous task execution
- **MariaDB**  
    Django's application database
- **Redis**  
    Object store for Django's cache, session and messaging systems & Celery results backend
- **RabbitMQ**  
    Message broker which brokers Celery tasks

[^1]: `Programming-Contest-Suite/src/contestsuite/settings.py`
[^2]: `Programming-Contest-Suite/src/contestsuite/flowerconfig.py`
