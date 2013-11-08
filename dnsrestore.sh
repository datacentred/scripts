#!/usr/bin/env bash

# Script to inject DNS records from a file created by dnsbackup.sh
# Takes two arguments - source file and relevant zone
# nick.jones@datacented.co.uk

SRC=$1
SERVER=ns0.sal01.datacentred.co.uk
ZONE=$2
KEY="/etc/bind/rndc.key"
UPDATE="/var/tmp/nsupdate"

# "Headers" for nsupdate
echo "server $SERVER" > $UPDATE
echo "zone $ZONE." >> $UPDATE

while read line
do
	echo "update add $line" >> $UPDATE
done < $SRC

# "Footer"
echo "send" >> $UPDATE

# Go!
nsupdate -k $KEY -v $UPDATE

