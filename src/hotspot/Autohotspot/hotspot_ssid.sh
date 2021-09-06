#!/bin/bash


#Change the Default Hotspot SSID and Password
if  [ ! -f "/etc/hostapd/hostapd.conf" ] ;then
    echo "A hotspot is not installed. No Password to change"
    exit 0
fi
HSssid=($(cat "/etc/hostapd/hostapd.conf" | grep '^ssid='))
HSpass=($(cat "/etc/hostapd/hostapd.conf" | grep '^wpa_passphrase='))
echo "Change the Hotspot's SSID and Password. press enter to keep existing settings"
echo "The current SSID is:" "${HSssid:5}"
echo "The current SSID Password is:" "${HSpass:15}"
echo "The new Hotspots SSID:" "$1"

echo "The new Hotspots password:" "$2"

if [ ! -z $1 ] ;then
    echo "Changing Hotspot SSID to:" "$1" 
    sed -i -e "/^ssid=/c\ssid=$1" /etc/hostapd/hostapd.conf
else
    echo "The Hotspot SSID is"  ${HSssid: 5}
fi
if [ ! -z $2 ] && [ ${#2} -ge 8 ] ;then
    echo "Changing Hotspot Password to:" "$2"
    sed -i -e "/^wpa_passphrase=/c\wpa_passphrase=$2" /etc/hostapd/hostapd.conf
else
    echo "The Hotspot Password is:"  ${HSpass: 15}
fi
echo ""
echo "The new setup will be available next time the hotspot is started"	
