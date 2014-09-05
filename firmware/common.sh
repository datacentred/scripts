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
