---
title: Configuration
layout: default
parent: Deployment
nav_order: 2
---

# Configuration

The PCS's main settings file[^1] and Flower settings file[^2] can be modified directly or with values specified through the use of environment variables. Environment variable values may be passed directly or as the contents of a file. In the latter case, the full path of the file should be passed as a variable's value. Environment variable values may be stored and passed as [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/).


### Default Values

Many of the default values used in the PCS's configuration files are designed for a Docker deployment similar to the examples in the [Docker Deployment]({{ site.url }}/deployment/docker/) section of this documentation. 

{: .important-title }
> Notation
>
> **(D)** debug mode `DEBUG=True`  
> **(P)** production mode `DEBUG=False` 

<hr>

## Django

The following variables, located in the main settings file[^1], map to various Django settings. A link to the relevant Django documentation is provided for each variable.

### General

Variable | Default | Description
---|---|---
SECRET_KEY | a long string[^3] | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECRET_KEY)
DEBUG | False | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-DEBUG) 
ALLOWED_HOSTS | [] | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts)
TIME_ZONE | America/New_York | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-TIME_ZONE)


### Cache

Variable | Default | Description
---|---|---
CACHE_LOCATION | redis://redis:6379/0 | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#location)
CACHE_TIMEOUT | **(D)** 0<br>**(P)** 300  | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#timeout)


### Database 

Variable | Default | Description
---|---|---
SQL_HOST | mariadb | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#host)
SQL_PORT | 3306 | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#port)
SQL_DATABASE | contestsuite | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#name)
SQL_USER | contestadmin | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#user)
SQL_PASSWORD | seminoles1! | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#password)
SQL_TIMEZONE | America/New_York | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#time-zone) 


### Email

Variable | Default | Description
---|---|---
EMAIL_BACKEND | **(D)** `django.core.mail.backends.console.EmailBackend`<br>**(P)** `django.core.mail.backends.smtp.EmailBackend` | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-backend)
EMAIL_HOST | None | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-host)
EMAIL_PORT | 587 | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-port)
EMAIL_HOST_USER | None | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-user)
EMAIL_HOST_PASSWORD | None | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-password)
EMAIL_USE_SSL | False | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-ssl)
EMAIL_USE_TLS | False | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-tls)
DEFAULT_FROM_EMAIL | acm@cs.fsu.edu | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email)

## Celery

The following variables, located in the main settings file[^1], map to various Celery settings. A link to the relevant Celery documentation is provided for each variable.

Variable | Default | Description
---|---|---
CELERY_BROKER | amqp://rabbitmq:5672 | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-broker_url)
CELERY_BACKEND | redis://redis:6379/1 | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-result_backend)
CELERY_TIMEZONE | America/New_York | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-timezone)

## Celery Beat

The following variables, located in the main settings file[^1], map to various Celery Beat settings. A link to the relevant Celery Beat documentation is provided for each variable.

Variable | Default | Description
---|---|---
CELERY_BEAT_SCHEDULE | `{}` | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-beat_schedule)

## Flower

The following variables, located in the Flower settings file[^2], map to various Flower settings. A link to the relevant Flower documentation is provided for each variable.

Variable | Default | Description
---|---|---
FLOWER_BROKER_API | http://rabbitmq:15672/api/vhost | [Docs](https://flower.readthedocs.io/en/latest/config.html#broker-api)
FLOWER_USER **(P)** | contestadmin | [Docs](https://flower.readthedocs.io/en/latest/config.html#basic-auth)
FLOWER_PASSWORD **(P)** | seminoles1! | [Docs](https://flower.readthedocs.io/en/latest/config.html#basic-auth)
FLOWER_COOKIE_KEY **(P)** | None | [Docs](https://flower.readthedocs.io/en/latest/config.html#cookie-secret)
FLOWER_URL_PREFIX **(P)** | flower | [Docs](https://flower.readthedocs.io/en/latest/config.html#url-prefix)

## Discord

The following variables, located in the main settings file[^1], map to various PCS specific settings required for integration with Discord.

Variable | Default | Description
---|---|---
ANNOUNCEMENT_WEBHOOK_URL | None | URL of Discord server's announcement channel webhook |

## Misc

The following variables, located in the main settings file[^2], map to miscellaneous PCS specific settings. A link to relevant documentation is provided for each variable.

Variable | Default | Description
---|---|---
DOMJUDGE_URL | https://domjudge.cs.fsu.edu/public | Full URL of the DOMjudge server. Used for PCS homepage contest server status card.
PCS_DOCS_URL | https://mmcinnestaylor.github.io/Programming-Contest-Suite | Base URL of the project's documentation website. Used to link registration guide and other manuals.
HASHID_FIELD_SALT | a long string[^4] | [Docs](https://github.com/nshafer/django-hashid-field#hashid_field_salt) The `django-hashid-field` library is used to hash sensitive PCS database model fields.
GTAG | None | [Google Analytics site tag](https://support.google.com/analytics/answer/12002338?hl=en)

[^1]: `Programming-Contest-Suite/src/contestsuite/settings.py`
[^2]: `Programming-Contest-Suite/src/contestsuite/flowerconfig.py`
[^3]: `86@j2=z!=&1r_hoqboog1#*mb$jx=9mf0uw#hrs@lw&7m34sqz`
[^4]: `0s97rx*t4%68jell&lw3^)97o*kr*+*2o^(76q)ix+ilc!4ax#`
