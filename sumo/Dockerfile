FROM ubuntu:20.04

WORKDIR /usr/src/app

RUN apt-get -qq update -y
RUN apt-get -qq install -y software-properties-common
RUN apt-get -qq install -y python3-pip
RUN add-apt-repository -y ppa:sumo/stable
RUN apt-get -qq update -y

#Install SUMO
RUN add-apt-repository ppa:sumo/stable -y
RUN apt-get -qq update -y
RUN apt-get -qq install -y sumo sumo-tools sumo-doc

#RUN apt-get -qq install -y sumo=1.4.0+dfsg1-1 sumo-tools sumo-doc
RUN pip3 install traci
COPY . .
ENV SUMO_HOME='/usr/bin/sumo/'