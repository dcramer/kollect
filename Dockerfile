# Use an official Python runtime as a parent image
FROM python:3.7-slim-stretch

# add our user and group first to make sure their IDs get assigned consistently
RUN groupadd -r kollect && useradd -r -m -g kollect kollect

ENV PATH /usr/src/zeus/bin:/root/.poetry/bin:$PATH

ENV NVM_DIR /usr/local/nvm
ENV NODE_ENV production

ENV PYTHONUNBUFFERED 1

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_VERSION 18.0

RUN mkdir -p /usr/src/kollect
WORKDIR /usr/src/kollect

RUN set -ex \
    && apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        gcc \
        git \
        gosu \
        libffi-dev \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        openssl \
        ssh \
        wget \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/0.12.10/get-poetry.py | python \
  && poetry config settings.virtualenvs.create false

RUN pip install "pip==$PIP_VERSION"


COPY pyproject.toml poetry.lock /usr/src/kollect/
RUN poetry install --no-dev

COPY . /usr/src/kollect
# ensure we've fully installed any changes
RUN poetry install --no-dev

ENV PATH /usr/src/kollect/bin:$PATH

# Make port 8000 available to the world outside this container
EXPOSE 8000

ENTRYPOINT ["docker-entrypoint"]

# Run Zeus
CMD ["gunicorn", "kollect.wsgi" "--log-file -"]
