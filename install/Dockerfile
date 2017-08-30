FROM debian:stretch

ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl

COPY main.sh .
RUN bash main.sh

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]