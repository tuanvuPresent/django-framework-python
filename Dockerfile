#FROM python:3.6-slim

#WORKDIR /usr/src/app

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1


#RUN pip install --upgrade pip  \
#    && pip install pipenv
#RUN apt update && apt install -y build-essential default-libmysqlclient-dev git

#COPY ./requirements.txt /usr/src/app/
#RUN pip install -r requirements.txt

#COPY . /usr/src/app/
#COPY ./entrypoint.sh /usr/src/app/
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# python alpine
FROM python:3.6-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip  \
    && pip install pipenv
RUN apk update \
    && apk add musl-dev mariadb-dev gcc  \
      build-base gcc python3-dev postgresql-dev musl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install wheel
COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache -r requirements.txt

COPY . /usr/src/app/
COPY ./entrypoint.sh /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
