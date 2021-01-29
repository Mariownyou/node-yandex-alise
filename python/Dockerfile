FROM python:3.8-alpine

WORKDIR /app
COPY . /app

EXPOSE 5000

RUN pip3 install -r requirements.txt
CMD FLASK_APP=api.py flask run --host="::"