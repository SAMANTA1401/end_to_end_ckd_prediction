FROM python:3.10-slim 

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
RUN echo MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
RUN echo MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3","app.py"]