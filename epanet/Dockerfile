FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update -yq
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -yq cmake
RUN apt-get install -yq curl wget build-essential python3-pip python3-dev libpq-dev netcat nano coreutils dos2unix

RUN cd /usr/local/bin
RUN ln -s /usr/bin/python3 python
RUN pip3 install --upgrade pip

WORKDIR /home
COPY ./EPANET-2.1.tar.gz .
RUN tar -xzf EPANET-2.1.tar.gz
WORKDIR "/home/EPANET-2.1/build/Linux"
RUN make
RUN make install

ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/EPANET-2.1/build/Linux"

WORKDIR /home
COPY ./epanet2-2.0.12.tar.gz .
RUN tar -xzf epanet2-2.0.12.tar.gz
WORKDIR "/home/epanet2-2.0.12"
RUN ./configure
RUN make
RUN make install

WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .
RUN dos2unix entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

WORKDIR /usr/src/app

RUN apt-get -qq update -y
RUN apt-get -qq install -y software-properties-common ssh openssh-server iputils-ping net-tools nano
RUN apt-get -qq install -y python3-pip
COPY ./keyfiles/id_rsa /root/.ssh/id_rsa
COPY ./keyfiles/id_rsa.pub /root/.ssh/id_rsa.pub
RUN chmod 600 /root/.ssh/id_rsa
COPY . .
RUN add-apt-repository -y ppa:sumo/stable
RUN apt-get -qq update -y
#Install SUMO
RUN add-apt-repository ppa:sumo/stable -y
RUN apt-get -qq update -y
RUN apt-get -qq install -y sumo sumo-tools sumo-doc
#RUN apt-get -qq install -y sumo=1.4.0+dfsg1-1 sumo-tools sumo-doc
RUN pip3 install traci

ENV SUMO_HOME='/usr/bin/sumo/'

#MATLAB
#ENV DEBIAN_FRONTEND noninteractive
#RUN apt-get -q update
#RUN apt-get install -q -y --no-install-recommends xorg unzip ca-certificates

#RUN mkdir /mcr-install
#RUN mkdir /opt/mcr
#WORKDIR /mcr-install

#COPY . .
#RUN wget -q https://ssd.mathworks.com/supportfiles/downloads/R2020b/Release/0/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2020b_glnxa64.zip
#RUN unzip -q MATLAB_Runtime_R2020b_glnxa64.zip
#RUN ./install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent
#ENV LD_LIBRARY_PATH /opt/mcr/v99/runtime/glnxa64:/opt/mcr/v99/bin/glnxa64:/opt/mcr/v99/sys/os/glnxa64:/opt/mcr/v99/extern/bin/glnxa64
#ENV XAPPLRESDIR /etc/X11/app-defaults
