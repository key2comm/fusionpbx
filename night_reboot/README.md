This file is built off the file that is already installed on the system located at  /usr/src/fusionpbx-install.sh/ubuntu/resources/reboot.sh

**All credit goes to the FusionPBX Team. I'm just modifying the script with some other options in it.

You have two options for the file. You only need one.

<hr>
reboot_phones.py will run through a list of vendors to try to get the phone to reboot. This is good if you have multiple vendor phones, snom, yealink etc. This one will try to reboot them all at once.  This might use a little more CPU if you have a lot of phones. If there are 5 vendors, it will try to reboot the extension five times with each vendor.

<hr>

reboot_one_brand.py will just reboot one brand of phones. Update line 20 vendors = ['yealink'] and input the vendor you want to reboot. This script is not limited to just one vendor. You can add two if you wish. Example would be if you wanted Yealink and Grandstream Phones. vendors = ['yealink', 'grandstream']

<hr>

Then you can add this into your crontab. You do not need root access on your system to run this.

Example of crontab assuming your user login is ubuntu. Please change to wahtever your home directory is for your user.
crontab -e #this will open the crontab editor
@midnight python3 /home/ubuntu/reboot_phones.py

Then press ctrl + o to save then ctrl + x to exit