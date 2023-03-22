# Download and install Matlab Compiler Runtime Version 9.9 (2020b)
#
# This docker file will configure an environment into which the Matlab compiler
# runtime will be installed and in which stand-alone matlab routines (such as
# those created with Matlab's deploytool) can be executed.
#

FROM debian:stretch-slim
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -q update
RUN apt-get install -q -y --no-install-recommends xorg unzip wget curl ca-certificates ssh openssh-server iputils-ping net-tools dos2unix
COPY ./ssh/sshd_config /etc/ssh/sshd_config
RUN echo 'root:matlab' | chpasswd
RUN mkdir /mcr-install
RUN mkdir /opt/mcr
WORKDIR /mcr-install
COPY ./power ./power
COPY ./run.sh ./run.sh
#COPY ./MATLAB_Runtime_R2020b_glnxa64.zip ./MATLAB_Runtime_R2020b_glnxa64.zip
#COPY . .
RUN wget -q https://ssd.mathworks.com/supportfiles/downloads/R2020b/Release/0/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2020b_glnxa64.zip
RUN unzip -q MATLAB_Runtime_R2020b_glnxa64.zip
RUN ./install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent
ENV LD_LIBRARY_PATH /opt/mcr/v99/runtime/glnxa64:/opt/mcr/v99/bin/glnxa64:/opt/mcr/v99/sys/os/glnxa64:/opt/mcr/v99/extern/bin/glnxa64
ENV XAPPLRESDIR /etc/X11/app-defaults
RUN chmod 777 power
COPY ./keyfiles/authorized_keys /root/.ssh/authorized_keys
RUN dos2unix /mcr-install/run.sh
ENTRYPOINT service ssh restart && bash
