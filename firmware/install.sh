#!/bin/bash

source common.sh

mkdir -p ${FWHOME}/ipmi/${IPMIFWVER}
mkdir -p ${FWHOME}/bios/${BIOSFWVER}
mkdir -p ${FWHOME}/nvram
mkdir -p /usr/local/bin/scripts/firmware

install -m 644 firmware/X8DTT220.ima ${FWHOME}/ipmi/${IPMIFWVER}
install -m 755 firmware/Yafuflash /usr/local/bin/scripts/firmware
install -m 644 bios_21b.bin ${FWHOME}/ipmi/${IPMIFWVER}/dcbios.bin
install -m 644 dcnvram_080714.bin ${FWHOME}/nvram/dcnvram.bin
