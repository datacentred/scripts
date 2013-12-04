BMC Firmware Flashing Utilities

==================
YAFUKCS:

Yafukcs is a tool used for flashing using KCS medium. 
The usage of the YafuKcs utility is shown below. 
This utility is used in DOS environment for flashing.

Usage: YafuKcs [OPTION] [FW_IMAGE_FILE] 

-?		Displays the utility usage 
-h		Displays the utility usage 

OPTION:
-info                 Displays information about current FW and new FW 
-auto                Option to do auto upgrade by comparing FMH 
-full,       	Option to do full upgrade 
-force-boot      Option to FORCE BootLoader upgrade during full upgrade 
		By default Boot Loader will be preserved
-c                    Option to preserve Config Module during full upgrade 
FW_IMAGE_FILE:
fw_image_file	 Firmware Image file name  

Eg. yafukcs -full x7sb3_rom025.ima


==================
YAFUFLASH:

YafuFlash is a tool used for flashing BMC using network and USB medium. 
The usage of the YafuFlash utility is shown below. 
This utility is used for flashing in both Linux and Windows environment.

Usage: Yafuflash [OPTION] [MEDIUM] [FW_IMAGE_FILE] 
Perform BMC Flash Update 
-?		 Displays the utility usage 
-h		 Displays the utility usage 

OPTION: 
-info                Displays information about current FW and new FW 
-auto               Option to do auto upgrade by comparing FMH 
-full,       	Option to do full upgrade 
-force-boot      Option to FORCE BootLoader upgrade during full upgrade 
		By default Boot Loader will be preserved
-c                    Option to preserve Config Module during full upgrade 
           
MEDIUM: 
-cd                 Option to use USB Medium 
-nw & -ip        Option to use Network Medium 
                     '-ip' Option to enter IP, when using Network Medium 

FW_IMAGE_FILE: 
fw_image_file	    Firmware Image file name.


Eg. yafuflash -full -cd x7sb3_rom025.ima

For Linux, tool: yafuflash; Library: libipmi.so.1, libipmi.so.1.0 

1. The file libipmi.so.1 should be accessible to linux system. 
Usually when running an application linux searches for the 
dependent libraries in the default locations like /usr/lib /lib folders.
 
2. Copy libipmi.so.1 to /lib or /usr/lib and run 'ldconfig'
OR 
copy libipmi.so.1 to some folder and issue the following command 
# LD_LIBRARY_PATH=<location_of_libipmi_so> ./Yafuflash
You may have to create a link to libipmi.so.1.0 (ln –sf libipmi.so.1.0 libipmi.so.1)

3. Run yafuflash just like in Windows.
  Eg. for network flashing: 
  #LD_LIBRARY_PATH=/root/linux_x86 ./Yafuflash -full -b -c -nw -ip 192.168.100.136 rom.ima
OR
  ./Yafuflash -full -b -c -nw -ip 192.168.100.136 -u ADMIN -p ADMIN rom.ima


===================
Dump from windows network flashing:

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

H:\downloads\fromsmc\smc\development\proprietary\software\YafuFlash\windows
\Release>Yafuflash.exe -nw -ip 172.16.99.122 -full -b rom-fromsmc.ima
-------------------------------------------------
YAFUFlash - Firmware Upgrade Utility (Version 1.1)
-------------------------------------------------
(C)Copyright 2008, American Megatrends Inc.
Please enter login information:
User      : ADMIN
Password  : *****
Creating IPMI session via network with address 172.16.99.122...Done Doing Full Firmware upgrade

************************************************************************
 WARNING!
        FIRMWARE UPGRADE MUST NOT BE INTERRUPTED ONCE IT IS STARTED.
************************************************************************
Upgrading Firmware Image : 100% done
Resetting the firmware..........

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

