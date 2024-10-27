FROM python:3.10-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip==24.0 \
   && pip install pipenv
RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev gcc -y

COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/
COPY ./entrypoint.sh /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
