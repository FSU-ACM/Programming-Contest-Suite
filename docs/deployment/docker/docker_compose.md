---
layout: default
title: Docker Compose
grand_parent: Deployment
parent: Docker
nav_order: 2
---

The following [Docker Compose](https://docs.docker.com/compose/) deployment, suitable for development and testing, is available in the repository [here](https://github.com/mmcinnestaylor/Programming-Contest-Suite/tree/main/deploy).

```yaml
services:
    django:
        build:
            context: ../
            args:
                REQUIREMENTS: requirements-dev.txt
        image: contestsuite:dev
        command: /docker/start.sh server debug
        environment:
            # Django
            DEBUG: 'True'

            # Database
            SQL_DATABASE: contestsuite
            SQL_USER: contestadmin
            SQL_PASSWORD: seminoles1!

            # Discord
            GUILD_ID: # Discord Server ID
        ports:
            - 8000:8000
        volumes:
            - ../src:/app
        networks:
            - contestsuite
        depends_on:
            - mariadb
            - redis
            - rabbitmq
            - celery_worker
        restart: unless-stopped
    celery_worker:
        image: contestsuite:dev
        command: /docker/start.sh worker debug
        environment:
            # Django
            DEBUG: 'True'

            # Database
            SQL_DATABASE: contestsuite
            SQL_USER: contestadmin
            SQL_PASSWORD: seminoles1!
            
            # Discord
            ANNOUNCEMENT_WEBHOOK_URL: # Webhook URL of the contest announcements channel
            BOT_CHANNEL_WEBHOOK_URL: # Webhook URL of the bot command channel
        volumes:
            - ../src:/app
        networks:
            - contestsuite
        depends_on:
            - mariadb
            - redis
            - rabbitmq
        restart: unless-stopped
    celery_beat:
        image: contestsuite:dev
        command: /docker/start.sh beat debug
        environment:
            # Django
            DEBUG: 'True'

            # Database
            SQL_DATABASE: contestsuite
            SQL_USER: contestadmin
            SQL_PASSWORD: seminoles1!
        volumes:
            - ../src:/app
        networks:
            - contestsuite
        depends_on:
            - mariadb
            - redis
            - rabbitmq
            - celery_worker
        restart: unless-stopped
    celery_flower:
        image: contestsuite:dev
        command: /docker/start.sh flower debug
        environment:
            # Django
            DEBUG: 'True'

            # Database
            SQL_DATABASE: contestsuite
            SQL_USER: contestadmin
            SQL_PASSWORD: seminoles1!
        ports:
            - 5555:5555
        volumes:
            - ../src:/app
        networks:
            - contestsuite
        depends_on:
            - mariadb
            - redis
            - rabbitmq
            - celery_worker
        restart: unless-stopped
    mariadb:
        image: mariadb:10.6-focal
        environment:
            MARIADB_DATABASE: contestsuite
            MARIADB_USER: contestadmin
            MARIADB_PASSWORD: seminoles1!
            MARIADB_ROOT_PASSWORD: rootpw
        volumes:
            - django_db:/var/lib/mysql
        networks:
            - contestsuite
    redis:
        image: redis:5-buster
        volumes:
            - redis:/data
        networks:
            - contestsuite
    rabbitmq:
        image: rabbitmq:3-management-alpine
        volumes:
            - rabbitmq:/var/lib/rabbitmq
        networks:
            - contestsuite       
volumes:
    django_db:
    redis:
    rabbitmq:
networks:
    contestsuite:
        name: contestsuite
```
