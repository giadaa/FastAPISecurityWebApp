#!/bin/bash

#download python3
sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel
sudo yum -y install wget
wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz
tar xvf Python-3.9.10.tgz
cd Python-*/
./configure --enable-optimizations
sudo make altinstall

#create our working directory if it doesnt exist
DIR="/home/ec2-user/security-tracker-app"
if [ -d "$DIR" ]; then
  echo "${DIR} exists"
else
  echo "Creating ${DIR} directory"
  mkdir ${DIR}
fi
