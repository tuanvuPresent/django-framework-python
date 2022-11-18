FROM python:3.6-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pip3 install wheel
RUN apt update && apt install -y build-essential default-libmysqlclient-dev git

COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
