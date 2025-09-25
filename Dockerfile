FROM python:3.12-slim
LABEL maintainer="ACM at FSU <contact@fsu.acm.org>"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ARG REQUIREMENTS=requirements.txt

RUN apt-get update \
  # Dependencies for building Python packages
  && apt-get install -y --no-install-recommends build-essential \
  # Translations dependencies
  && apt-get install -y gettext \
  # mysqlclient dependency 
  && apt-get install -y pkg-config \
  # MariaDB dependency
  && apt-get install -y libmariadb-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install requirements and create static file directories
RUN pip install --upgrade pip
COPY $REQUIREMENTS /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm -rf /tmp/requirements.txt \
  && useradd -U app_user \
  && install -d -m 0755 -o app_user -g app_user /app/static \
  && install -d -m 0755 -o app_user -g app_user /app/media \
  && install -d -m 0755 -o app_user -g app_user /app/media/contest_files \
  && install -d -m 0755 -o app_user -g app_user /app/media/ec_files \
  && install -d -m 0755 -o app_user -g app_user /app/media/team_files \
  && install -d -m 0755 -o app_user -g app_user /app/media/uploads

# Code and User Setup
USER app_user:app_user

COPY --chown=app_user:app_user scripts/docker/ docker/
RUN chmod +x docker/*.sh

WORKDIR /app

COPY --chown=app_user:app_user src .

# Docker Run Checks and Configurations
EXPOSE 8000

ENTRYPOINT [ "../docker/entrypoint.sh" ]
CMD [ "../docker/start.sh", "server" ]
