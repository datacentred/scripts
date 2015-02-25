#!/bin/bash
#this script is intended for people running this firmware update tool on fresh ubuntu installations
#run this then everything else should work out
apt-get install -y ipmitool flashrom nvramtool
modprobe ipmi_msghandler
modprobe ipmi_devintf
modprobe ipmi_si
echo "This machine will reboot to load all the ipmi goodness, press ctrl-c to cancel"
sleep 10
shutdown -r now