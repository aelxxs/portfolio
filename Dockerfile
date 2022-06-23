FROM python:3.9

RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD flask run --host=0.0.0.0