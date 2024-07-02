This file will connect to the FusionPBX Github repository located at https://github.com/fusionpbx/fusionpbx

Download the repostory to your server. Then it will copy everything from /fusion/resources/templates/provision and override the ones you have on your server. 

We do a lot of on premise servers and we always need to download certain provision templates that are not included when we first do a build so we designed a script to download and sync in one simple script.

**Note it will not sync, it will copy and replace your current files located in /var/www/fusionpbx/resources/templates/provision/. If you have any custom configs you should back them up.