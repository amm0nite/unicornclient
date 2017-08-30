FROM debian:stretch

ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl python3-dev

RUN curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
RUN python3 get-pip.py
RUN rm get-pip.py

RUN pip3 install -U pip
RUN pip3 install unicornclient

CMD ["unicornclient"]