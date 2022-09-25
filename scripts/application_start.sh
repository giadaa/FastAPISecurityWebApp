#!/bin/bash

#give permission for everything in the express-app directory
sudo chmod -R 777 /home/ec2-user/security-tracker-app

#navigate into our working directory where we have all our github files
cd /home/ec2-user/security-tracker-app

#install requirements.txt
pip3 install -r /home/ec2-user/security-tracker-app/requirements.txt

#start python app in the background
nohup python3.9 -m uvicorn main:app --reload &
