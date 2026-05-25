ARG PYTHON_VERSION=3.14-bookworm
ARG APP_HOME=/app
ARG DJANGO_SETTINGS_MODULE=config.settings

FROM python:${PYTHON_VERSION} AS builder
WORKDIR /wheels

RUN apt-get update && apt-get install -y --no-install-recommends \
      pkg-config build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --wheel-dir=/wheels -r /tmp/requirements.txt


FROM python:${PYTHON_VERSION} AS runtime-base
ARG APP_HOME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="${APP_HOME}/src:${PYTHONPATH}"

WORKDIR ${APP_HOME}

COPY --from=builder /wheels /wheels
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-index --find-links=/wheels -r /tmp/requirements.txt \
 && rm -rf /wheels


FROM runtime-base AS prod
ARG APP_HOME
ARG DJANGO_SETTINGS_MODULE

ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR ${APP_HOME}

COPY . ${APP_HOME}

RUN pip install --no-cache-dir "gunicorn==23.0.0"

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-lc", "exec gunicorn -k uvicorn.workers.UvicornWorker config.asgi:application -w 4 -t 1000 -b ${HOST}:${PORT}"]


FROM runtime-base AS dev
ARG APP_HOME
WORKDIR ${APP_HOME}

COPY . ${APP_HOME}

COPY run.sh /usr/local/bin/run
RUN chmod +x /usr/local/bin/run

CMD ["bash", "-lc", "tail -f /dev/null"]
