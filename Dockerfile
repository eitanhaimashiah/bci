FROM python:3.8

LABEL maintainer="Eitan-Hai Mashiah"

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN chmod +x /wait-for-it.sh

COPY . /bci
RUN pip install /bci
