#!/usr/bin/env bash

# Script to update BIOS and IPMI / BMC firmware
# on SuperMicro X8DTT series machines.

# nick.jones@datacentred.co.uk

## Versions
IPMIFWVER="2.20"
BIOSFWVER="2.1b"

## Filesystem locations
FWHOME=/usr/local/lib/firmware
### IPMI Firmware
IPMIFW=$FWHOME/ipmi/$IPMIFWVER/X8DTT220.ima
### BIOS Firmware.  Note that this should be a dump (via flashrom) from a configured
### machine, and should match the NVRAM dump taken below.
BIOSFW=$FWHOME/bios/$BIOSFWVER/dcbios.bin
### NVRAM settings.  See above.
NVRAM=$FWHOME/nvram/dcnvram.bin

## Tools
YAFUHOME=/usr/local/bin/yafuflash
IPMITOOL=$(which ipmitool)
FLASHROM=$(which flashrom)
NVRAMTOOL=$(which nvramtool)

function check_ipmi_ver {
	# Checks whether the current IPMI firmware revision matches what's defined in $IPMIFWVER
	if [ $($IPMITOOL mc info | grep 'Firmware Revision' | awk '{ print $4 }') != $IPMIFWVER ]; then
		return 1
	fi
}

function set_usb {
	# For the IPMI firmware update to work locally, the BMC has to be in 'attach' mode
	echo "Setting BMC USB interface to 'attach' mode... "
	$IPMITOOL raw 0x30 0x70 0x0b 0x0
	echo "... done!"
}

function update_ipmi {
	# Updates IPMI firmware to version passed as $1
	echo "Beginning IPMI firmware update process, hit Ctrl-C to cancel... "
	sleep 5
	LD_LIBRARY_PATH=$YAFUHOME:$LD_LIBRARY_PATH $YAFUHOME/Yafuflash -cd -full $1
	echo "... done!"
}

function set_ipmi_dedicated {
	# By default, IPMI will attempt to 'share' the primary NIC instead of using the dedicated LAN
	# interface.  This sets it to the latter.
	echo "Setting IPMI network interface to 'dedicated'... "
	$IPMITOOL raw 0x30 0x70 0xc 1 1 0
	echo "... done! "
}

function update_bios {
	# Updates motherboard BIOS to version passed as $1
	echo "Beginning BIOS update process, hit Ctrl-C to cancel... "
	sleep 5
	$FLASHROM -w $1
	echo "... done!"
}

function verify_bios {
	# Function to verify current BIOS
	# Returns 0 if successful
	echo "Verifying BIOS against $1 ..."
	$FLASHROM -v $1 
}

function copy_bios_settings {
	# Copies BIOS settings, requires 'nvram' LKM to loaded and /dev/nvram present
	# We don't check for this as it's part of our base image.
	# Also needs 'nvramtool' to work properly.
	echo "Copying BIOS settings... "
	$NVRAMTOOL -B $NVRAM
	echo "... done!"
}

case $1 in
	check_ipmi)
		check_ipmi_ver
		;;
	check_bios)
		verify_bios $BIOSFW
		;;
	update_ipmi)
		set_usb
		update_ipmi $IPMIFW
		set_ipmi_dedicated
		;;
	update_bios)
		update_bios $BIOSFW
		copy_bios_settings
		;;
	full)
		# Full check / update where necessary process for BIOS and IPMI firmware
		# Check IPMI version, if it's not what we expect then we upgrade
		if ! check_ipmi_ver; then
			echo "IPMI firmware version mismatch, upgrading to $IPMIFWVER"
		 	set_usb
		 	update_ipmi $IPMIFW
		 	set_ipmi_dedicated
		fi
		# Same for BIOS version, check against known good file and if there's any mismatch we upgrade
		if ! verify_bios $BIOSFW; then
		 	update_bios $BIOSFW
		 	copy_bios_settings
		fi
		;;
	*)
		echo "Usage: $0 {check_ipmi|check_bios|update_ipmi|update_bios|full}"
		;;
esac
