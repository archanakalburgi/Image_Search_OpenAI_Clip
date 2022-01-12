FROM python:3.8-slim-buster

RUN apt-get update -y  && apt-get install -y git && apt-get install -y build-essential
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .
EXPOSE 5550
CMD [ "python", "app.py" ]

