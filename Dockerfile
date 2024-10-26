FROM python:3.8-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip==23.2.1 \
   && pip install pipenv
RUN apt update && apt install -y build-essential default-libmysqlclient-dev git

COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/
COPY ./entrypoint.sh /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
