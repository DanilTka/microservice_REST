FROM python:3.8

WORKDIR /usr/scr/microservice_REST

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt .

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev

RUN python -m venv . && \
    ls && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .


RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
