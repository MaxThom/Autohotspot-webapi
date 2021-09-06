#!/bin/bash

if [ ! -f "/etc/systemd/system/autohotspot.service" ] ;then
    echo "No Autohotspot script installed, unable to continue"
    exit 0
fi
Aserv=($(cat /etc/systemd/system/autohotspot.service | grep "ExecStart="))
wi=($(cat ${Aserv: 10} | grep wifidev=))
eth=($(cat ${Aserv: 10} | grep ethdev=))

wifidev=${wi[0]: 9:-1} #wifi device name from active autohotspot/N script
ethdev=${eth[0]: 8:-1} #Ethernet port to use with IP tables

createAdHocNetwork_N() #for Internet routed Hotspot
{
    #receive IP as $1
    echo "Creating Hotspot with Internet"
    ip link set dev "$wifidev" down
    ip a add $1 brd + dev "$wifidev"
    ip link set dev "$wifidev" up
    dhcpcd -k "$wifidev" >/dev/null 2>&1
    iptables -t nat -A POSTROUTING -o "$ethdev" -j MASQUERADE
    iptables -A FORWARD -i "$ethdev" -o "$wifidev" -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -A FORWARD -i "$wifidev" -o "$ethdev" -j ACCEPT
    systemctl start dnsmasq
    systemctl start hostapd
    echo 1 > /proc/sys/net/ipv4/ip_forward
}

createAdHocNetwork_D() #For non Internet Routed Hotspot
{
    echo "Creating Hotspot direct - no Internet"
    ip link set dev "$wifidev" down
    ip a add $1 brd + dev "$wifidev"
    ip link set dev "$wifidev" up
    dhcpcd -k "$wifidev" >/dev/null 2>&1
    systemctl start dnsmasq
    systemctl start hostapd
}

get_HS_IP() #get ip address from current active hotspot script
{
    #add check that the service is enabled, otherwise exit
    Aserv=($(cat /etc/systemd/system/autohotspot.service | grep "ExecStart=")) #which hotspot is active?
    if [ ${Aserv: -4} = "spot" ];then #Direct
        ipline=($(cat /usr/bin/autohotspot | grep "ip a add"))
        createAdHocNetwork_D "${ipline[3]}" 
    elif [ ${Aserv: -4} = "potN" ];then #Internet
        ipline=($(cat /usr/bin/autohotspotN | grep "ip a add"))
        createAdHocNetwork_N "${ipline[3]}"
    else
        echo "The Autohotspot is disabled or not installed"
        echo "unable to force a switch."
        exit 0
    fi
}

#Create Hotspot or connect to valid wifi networks
echo 0 > /proc/sys/net/ipv4/ip_forward #deactivate ip forwarding

if systemctl status hostapd | grep "(running)" >/dev/null 2>&1
then
    echo "Hotspot already active"
    echo "Switching to Network Wifi if it is available"
    echo "this takes about 20 seconds to complete checks"
    systemctl restart autohotspot.service    
elif { wpa_cli status | grep "$wifidev"; } >/dev/null 2>&1
then
    echo "Cleaning wifi files and Activating Hotspot"
    wpa_cli terminate >/dev/null 2>&1
    ip addr flush "$wifidev"
    ip link set dev "$wifidev" down
    rm -r /var/run/wpa_supplicant >/dev/null 2>&1
    get_HS_IP
    else #Neither the Hotspot or Network is active
    get_HS_IP
fi
