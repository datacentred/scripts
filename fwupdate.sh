#!/usr/bin/env bash

# Script to update BIOS and IPMI / BMC firmware
# nick.jones@datacentred.co.uk

FWHOME=/usr/local/lib/firmware
IPMIFW=$FWHOME/X8DTT220.ima
BIOSFW=$FWHOME/dc_compute.bios
NVRAM=$FWHOME/nvram.bin
YAFUHOME=/usr/local/bin/yafuflash
IPMITOOL=$(which ipmitool)
FLASHROM=$(which flashrom)

function set_usb {
	echo "Setting USB to 'attach' mode... "
	$IPMITOOL raw 0x30 0x70 0x0b 0x0
	echo "... done!"
}

function update_ipmi {
	echo "Beginning IPMI firmware update process, hit Ctrl-C to cancel... "
	sleep 5
	echo LD_LIBRARY_PATH=$YAFUHOME:$LD_LIBRARY_PATH $YAFUHOME/Yafuflash -cd -full $1
}

function set_ipmi_dedicated {
	echo "Setting IPMI network interface to 'dedicated'... "
	$IPMITOOL raw 0x30 0x70 0xc 1 1 0
	echo "... done!"
}

function update_bios {
	echo "Beginning BIOS update process, hit Ctrl-C to cancel... "
	sleep 5
	$FLASHROM -w $1
	echo "... done!"
}

function verify_bios {
	echo "Verifying BIOS against $1 ..."
	$FLASHROM -v $1
}

function copy_bios_settings {
	echo "Copying BIOS settings... "
	dd if=$NVRAM of=/dev/nvram
	echo "... done!"
}

set_usb
update_ipmi $IPMIFW
set_ipmi_dedicated
update_bios $BIOSFW
verify_bios $BIOSFW
copy_bios_settings

