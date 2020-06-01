FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install -y npm
RUN apt-get install -yq nodejs build-essential
RUN npm install -g npm@latest

EXPOSE 5000 8000 8080

ADD scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod 755 wait-for-it.sh

ADD requirements.txt /requirements.txt
RUN pip3.8 install -r /requirements.txt

ADD bci /bci

WORKDIR bci/gui/app
RUN npm install
RUN npm install react react-dom react-router-dom bootstrap
RUN npm run build
WORKDIR /

ENV BLOB_DIR='/bcifs'