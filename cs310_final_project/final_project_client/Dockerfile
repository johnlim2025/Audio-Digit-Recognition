FROM python:3.11-alpine3.20

RUN apk update && apk upgrade
RUN apk add --no-cache bash

RUN echo "export HISTFILE=/dev/null" >> /etc/profile

RUN adduser -S user -G users -D

RUN pip3 install requests
RUN pip3 install jsons 