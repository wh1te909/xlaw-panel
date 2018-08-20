#!/bin/bash
FILE="/home/steam/xlawpanel/xlaw-panel/adminpanel/admin_files/admins_simple.ini"
DIR1="/home/steam/csgo/csgo/addons/sourcemod/configs/"
DIR2="/home/steam/csgo2/csgo/addons/sourcemod/configs/"
DIR3="/home/steam/csgo3/csgo/addons/sourcemod/configs/"
DIR4="/home/steam/csgo4/csgo/addons/sourcemod/configs/"

for i in dallas xlaw xeast xchi xfrank xlatwo xfranktwo finkone
do
/usr/bin/scp ${FILE} steam@${i}:${DIR1}
/usr/bin/scp ${FILE} steam@${i}:${DIR2}
done

for i in xatla xnew
do
/usr/bin/scp ${FILE} steam@${i}:${DIR1}
/usr/bin/scp ${FILE} steam@${i}:${DIR2}
/usr/bin/scp ${FILE} steam@${i}:${DIR3}
/usr/bin/scp ${FILE} steam@${i}:${DIR4}
done