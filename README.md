# Programming Contest Suite

The Programming Contest Suite (PCS) is a set of tools for running [ICPC](https://icpc.global) style programming competitions hosted by the [Association for Computing Machinery Florida State University Student Chapter](https://fsu.acm.org). The suite is designed to work with a [DOMJudge](https://www.domjudge.org/) jury system by facilitating contest registration and management, generating contestant data files required by DOMjudge, and processing contest results. 

# Features

### Contestants

- **Registration**: quickly register for an upcoming programming contest, or as a walk-in participant on contest day
- **Teams**: form and manage teams of up to three individuals, all within the profile management dashboard
- **Courses**: select any available FSU classes in which the individual is registered in order to receive extra credit for contest participation (subject to instructor approval)
- **Matchmaking**: Discord powered matchmaking service to assist in team formation
- **Check-in**: simple student-ID card based check-in

### Organizers

- **Announcements**: create public contest announcements viewable in the web app and optionally distributed via email and/or Discord webhook
- **Tools**: easy-to-use faculty and course data input file generation utilities
- **Courses**: one-click upload and processing of faculty + course data files in Django Admin
- **DOMjudge**: one-click generation of contestant data input files used to initialize DOMjudge
- **Participation**: one-click generation of contestant participation files invididually curated for each faculty member
- **Volunteer Management**: volunteer role assignment interface and volunteer check-in monitoring 

### Volunteers

- **Check-in**: easy-to-use dedicated volunteer check-in interface

### Faculty Members

- **Integration**: automatic notification post contest of participation file availability, accessible via secure download

# Installation

Simply clone this repository: 

	git clone https://github.com/FSU-ACM/Programming-Contest-Suite.git


Alternatively, download one of the versions available on the [releases](https://github.com/FSU-ACM/Programming-Contest-Suite/releases) page.  

# Deployment

There are many ways to [deploy Django](https://docs.djangoproject.com/en/4.2/howto/deployment/). The project has been extenively tested with and includes files for deploying using [Docker](https://www.docker.com/).

### Docker

Please reference `docs/docker/` for image creation and usage documentation. Pre-built images are available in the project's [Docker Hub repository](https://hub.docker.com/r/acmfsu/contestsuite). Reference `deploy/docker-compose.yml` for an example deployment intended for [Docker Compose](https://docs.docker.com/compose/) and suitable for local development and testing purposes.

#### Default Superuser
user: `contestadmin`  
pass: `seminoles1!`

A default superuser account is created when the container connects to an empty database. The default password should be changed to secure the account.

### Production

The default values of `SECRET_KEY` and `HASHID_FIELD_SALT` are not safe for production use and should be changed. Django secret key generators are readily available online.

### Quick-start

The following steps outline running the PCS outside of a Docker context. This is minimally sufficient for development or internal testing, but not for a production deployment. 

#### Install Project Requirements

Package manifest files are located in the repository's root directory. The `Pipfile` can be used to set up a virtual environment using [Pipenv](https://pipenv.pypa.io/en/latest/), which is also used to generate a `pip` compatible `requirements.txt` . 

#### Spin-up Support Services

Using the default configuration, Django and Celery rely on instances of MariaDB, Redis, and RabbitMQ. Server addresses and credentials should be passed to Django and Celery via envronment variables. 

#### Start Django & Celery 

The following assumes `Programming-Contest-Suite/src` is the working directory.

##### Web Server

	gunicorn contestsuite.wsgi:application

##### Celery Worker

	celery -A contestsuite worker

##### Celery Beat

	celery -A contestsuite beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Documentation

All project documentation is available in `docs/`, and on our [documentation website](https://fsu-acm.github.io/Programming-Contest-Suite/).

# Contributing

We welcome contributions to the project! Check out `CONTRIBUTING.md` to learn how to get started.

### Our Contributors

- [Marlan McInnes-Taylor](https://github.com/mmcinnestaylor) *Creator*
- [Daniel Riley](https://github.com/danielmriley)
- [Preston Horne](https://github.com/prestonmhorne)
- [Hoang Vu](https://github.com/hoangvu5)
- [Aidan Collins](https://github.com/getsbuffer)
