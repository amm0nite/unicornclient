FROM debian:jessie

ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl

COPY install/main.sh .
RUN bash main.sh

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]