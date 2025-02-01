# syntax=docker/dockerfile:1

FROM python:3-alpine AS build-stage

RUN mkdir /svc
WORKDIR /svc
COPY requirements.txt /svc

# Install required apk packages
RUN apk add --no-cache --update  \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev \
    g++ \
    git && \
    pip install --upgrade pip

# Build dependencies
RUN pip wheel -r /svc/requirements.txt --wheel-dir=/svc/wheels

FROM python:3-alpine

ENV PYTHONUNBUFFERED=TRUE

WORKDIR /usr/src/app
COPY . .
# RUN pip install -r requirements.txt --no-cache-dir
COPY --link --from=build-stage /svc/wheels /usr/src/app/wheels
RUN pip install --no-index --find-links=/usr/src/app/wheels -r requirements.txt
RUN pip install --no-cache-dir uvloop || echo "Not using uvloop"

ENV TCP_NODELAY=1
ENV TCP_QUICKACK=1

EXPOSE 8080
ENTRYPOINT [ "/usr/src/app/main.py" ]
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 CMD test -f /usr/src/app/alive.txt && rm /usr/src/app/alive.txt && echo "Healthy" || echo "Unhealthy"
