FROM python:3.7

WORKDIR /app
ARG requirements=requirements/production.txt

ADD . /app

RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -r $requirements
RUN apt -y update && apt -y upgrade && apt -y install libvips && apt-get install libpng-dev && apt-get install zlib1g-dev
RUN CC="cc -mavx2" pip install -U --force-reinstall pillow-simd