#!/bin/bash

set -euxo pipefail

# UPDATE PACKAGE MANAGERS
apt-get update
apt update

# DO APT INSTALLS
apt install --no-install-recommends \
  vim \
  git \
  openssh-client \
  libopenni-dev \
  apt-utils \
  python-pip \
  python-dev \

# DO APT-GET INSTALLS
apt-get -y install \
  ipython \
  ipython-notebook \
  libglib2.0-0 

apt-get install \
  libgtk2.0-dev \
  libsm6 \
  libxrender1 \
  libfontconfig1 \
  python-tk \
  ffmpeg

# DO PIP INSTALLS
pip install --upgrade pip==9.0.3
pip install -U setuptools

pip install \
  numpy \
  jupyter \
  opencv-python \
  pandas \
  torch==1.0.0 \
  torchvision 
