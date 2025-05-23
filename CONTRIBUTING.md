# Contributors Guide
Thanks for your interest in contributing to the project! As of January 2024, development has been permanently handed off to the ACM at FSU chapter. Please visit [FSU-ACM/Programming-Contest-Suite](https://github.com/FSU-ACM/Programming-Contest-Suite) for the latest version of the project, and up-to-date contribution information.

## Frameworks and Tools

Name | Context | Links
---|---|---
Django | Web framework | [Get Started](https://www.djangoproject.com/start/), [Documentation](https://docs.djangoproject.com/en/4.2/)
Celery | Async task execution, monitoring, scheduling | [Introduction](https://docs.celeryq.dev/en/stable/getting-started/introduction.html), [Documentation](https://docs.celeryq.dev/en/stable/index.html)
MariaDB | Django/Celery database backend | [About](https://mariadb.org/about/), [Documentation](https://mariadb.org/documentation/)
RabbitMQ | Celery broker | [Get Started](https://www.rabbitmq.com/#getstarted), [Documentation](https://www.rabbitmq.com/documentation.html)
Redis | Caching, session store, task result backend | [Get Started](https://redis.io/docs/get-started/)
Bootstrap | UI design | [Documentation](https://getbootstrap.com/docs/4.5/getting-started/introduction/)
Pipenv | Env virtualization, reqirements management | [Documentation](https://pipenv.pypa.io/en/latest/)

## Repository Overview

```
Programming-Contest-Suite/
├── deploy/
├── docs/
├── scripts/
├── src/
├── utils/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── requirements-dev.txt
└── requirements.txt
```

- `deploy`: example deployment files useful for development and testing
- `docs`: project documentation  
- `scripts`: shell scripts for executing various project services 
- `src`: project source code 
- `utils`: helper tools for input file creation
- `.dockerignore`: specifies files and directories ignored by `docker build` 
- `.gitignore`: specifies files and directories ignored by `git`
- `Dockerfile`: specifies the construction of the project's Docker image
- `Pipfile`: high level project requirements file used by Pipenv
- `Pipfile.lock`: the full project requirements built from the `Pipfile`
- `requirements-dev.txt`: project requirments for development and debug
- `requirements.txt`: project requirements for production

## Source Overview

```
Programming-Contest-Suite/
└── src/
    ├── announcements/
    ├── assets/
    ├── checkin/
    ├── contestadmin/
    ├── contestsuite/
    ├── core/
    ├── lfg/
    ├── manager/
    ├── media/
    ├── register/
    ├── static/
    ├── templates/
    └── manage.py
```

- `announcements`: display and distribute contest announcements
- `assets`: static files utilized project-wide
- `checkin`: contest day check-in
- `contestadmin`: contest administration interface
- `contestsuite`: settings directory for Django and Celery
- `core`: site's public facing pages
- `lfg`: Looking For Group service
- `manager`: user profile and team management 
- `media`: target directory for files generated by or uploaded to the PCS (placeholder dir)
- `register`: user account registration and team creation
- `static`: target directory for all project static files upon deployment (placeholder dir)
- `templates`: target directory for all project HTML templates upon deployment
- `manage.py`: Django management entrypoint

## Testing & Development Server 

`deploy/docker-compose.yml` contains an example deployment intended for [Docker Compose](https://docs.docker.com/compose/) and suitable for local testing and development. 

If you are running the development deployment for the first time, or have made any changes to the project's Celery tasks, run:  

    docker compose build  

Launch the project:  

    docker compose up

NOTE: In order to monitor the debug logs, as well as view any emails the system sends while in debug, it is suggested to NOT use the `-d` flag with the `docker compose up` command.

## Project Requirements

### Initialize Virtual Environment

```
# Programming-Contest-Suite/

pipenv install
```

### Update `requirements.txt`

#### Production

```
# Programming-Contest-Suite/

pipenv requirements > requirements.txt
```

#### Development

```
# Programming-Contest-Suite/

pipenv requirements --dev > requirements-dev.txt
```

## Documentation

All project documentation is located in `docs/`. We utilize the [Just the Docs](https://just-the-docs.github.io/just-the-docs/) Jekyll theme to style our documentation in Github Pages.

## Versioning

We use something similar to [SemVer](https://semver.org/):

  - MAJOR version for significant codebase rewrites.
  - MINOR version for localized changes, e.g. adding a new feature.
  - PATCH version for any adjustment to `main` codebase, e.g. bugfix.
