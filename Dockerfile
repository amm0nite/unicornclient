FROM debian:buster

ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl python3-dev

COPY /  /root/unicornclient
WORKDIR /root/unicornclient

ENV PYTHONENV prod

CMD ["python3", "-u", "-m", "unicornclient.client"]
