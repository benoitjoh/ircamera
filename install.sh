#!/bin/bash

# install motion
sudo apt -y install motion htop
sudo cp conf/motion.conf /etc/motion
 
# install the lichtcontrols
cp source/lightcontrol.py ~/
sudo cp conf/lightcontrol.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable lightcontrol.service
sudo systemctl start lightcontrol.service
