#!/bin/bash

#Change the Default Hotspot SSID and Password
if  [ ! -f "/etc/hostapd/hostapd.conf" ] ;then
    echo "A hotspot is not installed. No Password to change"
    exit 0
fi
HSssid=($(cat "/etc/hostapd/hostapd.conf" | grep '^ssid='))
HSpass=($(cat "/etc/hostapd/hostapd.conf" | grep '^wpa_passphrase='))
echo "The current SSID is:" "${HSssid:5}"
echo "The current SSID Password is:" "${HSpass:15}"
echo "The new Hotspots SSID:" "$1"
echo "The new Hotspots password:" "$2"

if [ ! -z $1 ] ;then
    sed -i -e "/^ssid=/c\ssid=$1" /etc/hostapd/hostapd.conf
fi
if [ ! -z $2 ] && [ ${#2} -ge 8 ] ;then
    sed -i -e "/^wpa_passphrase=/c\wpa_passphrase=$2" /etc/hostapd/hostapd.conf
fi
echo ""
echo "The new setup will be available next time the hotspot is started"	
