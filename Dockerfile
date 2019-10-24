FROM python:3

LABEL maintainer="bmistry12 <bmistry@hotmail.co.uk>" 

ARG arg_HOME=/opt/sonos-huter
ARG arg_INTERFACE=eth0
ENV HOME=$arg_HOME
ENV INTERFACE=$arg_INTERFACE

RUN mkdir -p ${HOME}
COPY sonos.py ${HOME}/sonos.py
COPY requirements.txt ${HOME}/requirements.txt

WORKDIR ${HOME}

RUN pip install -r requirements.txt

CMD [ "python", "sonos.py", "-i", ${INTERFACE}]