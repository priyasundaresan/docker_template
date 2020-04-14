FROM nvidia/cuda:8.0-devel-ubuntu16.04

RUN apt-get update

WORKDIR /home/$USER_NAME

COPY ./install_dependencies.sh /tmp/install_dependencies.sh
RUN yes "Y" | /tmp/install_dependencies.sh
