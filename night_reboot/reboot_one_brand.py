import os
import shutil
import time
import csv

temp_reboot_file = "/tmp/reboot.csv"

check_file_tmp = os.path.isfile(temp_reboot_file)
if check_file_tmp == True:
	os.remove(temp_reboot_file)
time.sleep(5)
print("Checking all the Phone Registrations, and exporting to a CSV file in /tmp/reboot.csv")
os.system('fs_cli -x "show registrations" > /tmp/reboot.csv')

# Vendors is an array where it will add the vendor at the end of the fs_cli. If you have different brands of phones
# this will solve making multiple scripts. This will do them all. If you are using a vendor that is not listed,
# you can add them into the vendors array as 'vendor' then save.
vendors = ['yealink']

with open(temp_reboot_file, mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Skip the header row and remove the last three rows
    rows_to_process = list(csv_reader)[1:-3] 
    
    for row in rows_to_process:
        # Check if the row has at least two columns
        if len(row) >= 2:
            # Extract the first two columns
            reg_user = row[0]
            realm = row[1]
            
            # Iterate through the list of vendors
            for vendor in vendors:
                # Construct the command string
                command = f'eval \'fs_cli -x "luarun app.lua event_notify internal reboot {reg_user}@{realm} {vendor}"\''
                
                # Execute the command using os.system
                os.system(command)
                
                # Optionally, print confirmation or any other output
                print(f"Executed command for reg_user: {reg_user}, realm: {realm}, vendor: {vendor}")
        else:
            print("Something went wrong:", row)
