#Make sure that you have python3-git installed on your Server debian apt-get install python3-git
import os
import shutil
import time
import csv

temp_reboot_file = "/tmp/reboot.csv"

check_file_tmp = os.path.isfile('temp_reboot_file')
if check_file_tmp == True:
	os.remove(temp_reboot_file)
time.sleep(5)
print("Checking all the Phone Registrations, and exporting to a CSV file in /tmp/reboot.csv")
os.system('fs_cli -x "show registrations" > /tmp/reboot.csv')

phone_brand = ["yealink", "grandstream", "cisco", "polycom"]

#with open('/tmp/reboot.csv', mode='w') as reg_phones:
#	csvRegPhones = csv.reader(temp_reboot_file)