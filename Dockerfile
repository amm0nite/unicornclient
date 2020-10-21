FROM debian:buster

ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl python3-dev python3-pip

COPY /  /root/unicornclient
WORKDIR /root/unicornclient

RUN pip3 install -r requirements.txt

ENV PYTHONENV prod

CMD ["python3", "-u", "-m", "unicornclient.client"]
