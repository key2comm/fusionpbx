#Make sure that you have python3-git installed on your Server debian apt-get install python3-git
from __future__ import annotations
import git
from pathlib import Path
from git import Repo
from git.remote import RemoteProgress
import os
import shutil
import time

class Progress(RemoteProgress):
    def update(self, *args):
        print(self._cur_line)

print("Checking if there is an existing temp folder")
##Making sure there is not already a temp folder in place or it will cause an issue
check_tmp = os.path.exists('/tmp/git_fusionpbx')
if check_tmp == True:
        print("Existing temp folder detected. Deleting before we can proceed")
        shutil.rmtree('/tmp/git_fusionpbx/')
time.sleep(10)
print("Downloading FusionPBX Git Repo to the /tmp/ folder")

temp_folder = "/tmp/git_fusionpbx"
project_url = "https://github.com/fusionpbx/fusionpbx"
time.sleep(5)
git.Repo.clone_from(project_url, temp_folder, progress=Progress())
print("Finish downloading Repo")

#If you want to put this into a cront job. either delete the next 2 lines or put a # in front of them. This will remove the confirmation process. 
confirm = input("Please confirm you wish to orverride your Live Direcotry for the Provision Folder. This will delete any custom template fles for phones.   yes | no \n")
if confirm  == "yes":
        print("Copying templates provision from Repo to your Live Directory")

source = "/tmp/git_fusionpbx/resources/templates/provision"
dest = "/var/www/fusionpbx/resources/templates/provision"

shutil.copytree(source, dest, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=True)
print("We have updated all the Provision files from GitHub!. You are up to date\n")
print("We now have to change the permission of all those folders. So we do not cause any issues\n")
time.sleep(3)
os.system('chown -R www-data:www-data /var/www/fusionpbx/resources/templates/provision/')
print("We have changed the ownership of the files and folders correctly")
print("Deleting files from /tmp")
shutil.rmtree('/tmp/git_fusionpbx/')
print("Everything is done. The script has downloaded the templates/provision folder into the live direcotry\n Everything is done now. Enjoy")

if confirm == "no":
        print("Stopping the process. Nothing more will happen")
