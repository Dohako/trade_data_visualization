FROM python-3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get upgrade -y \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/