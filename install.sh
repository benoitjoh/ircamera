#!/bin/bash
if [ "$(whoami)" != "pi" ]
   then echo '[ERR] script must run in context of user pi!' && exit 1
fi

# copy some files
cp conf/mask.pgm /home/pi
cp source/lightcontrol.py /home/pi
sudo cp conf/lightcontrol.service /etc/systemd/system




# install motion
sudo apt-get -y install motion htop
sudo cp conf/motion.conf /etc/motion

# create outputdirectory and make it accessible for user motion
pushd /var/lib
if [ ! -d "motion" ]
    then sudo mkdir motion
fi
sudo chmod 777 motion
sudo chown motion motion
cd motion
sudo -u motion mkdir pict

popd

# create log directory and make it accessible for user motion
pushd /var/log/
if [ ! -d "motion" ]
    then sudo mkdir motion
fi
sudo chmod 777 motion
sudo chown motion motion

popd

# install the lichtcontrols
sudo systemctl daemon-reload
sudo systemctl enable lightcontrol.service
sudo systemctl start lightcontrol.service
