FROM python:3.7

WORKDIR /app
ARG requirements=requirements/production.txt

ADD . /app

RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -r $requirements
RUN apt -y update && apt -y upgrade && apt -y install libvips