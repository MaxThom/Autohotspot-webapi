# Hostspot 

## API Controller
The controller offers only one endpoint to make different actions. Simply send json with the command and parameters.

### Get http://10.0.0.5/api/hotspot
1. Display known networks
```json
{
    "command": "display_networks"
}
```
2. Add or update networks
```json
{
    "command": "add_wifi",
    "ssid": "<name>",
    "psk": "<password>"
}
```
3. Display hotspot configuration
```json
{
    "command": "display_hotspot_ssid"
}
```
4. Update hotspot configuration
```json
{
    "command": "hotspot_ssid",
    "ssid": "<name>",
    "psk": "<password>"
}
```
5. Force device to switch to hotspot or wifi
```json
{
    "command": "force_hs_wifi"
}
```
6. Display the connected network
```json
{
    "command": "display_current_network"
}
```

#
## AutoHotspot

Refer to their website for full documentation and installation. 

### Autohotspot with No Internet for connected devices

This option create a hotspot where connected devices have no internet connection even if an ethernet cable is connected.
This has been designed so you can access only the Pi from a Laptop, tablet or phone.
The default hotspot SSID will be RPiHotspot with a password of 1234567890
Once a connection to the hotspot has been made you can access the Raspberry Pi via ssh & VNC with
- ssh pi@10.0.0.5
- vnc: 10.0.0.5::5900
- for webservers use http://10.0.0.5/

### Add or Change a WiFi network (SSID)
If you are using either of the autohotspot setups in hotspot modes and wish to connect to a local WiFi network. You will be unable to scan for any networks as the desktop wifi option will be disabled, shown as red crosses. You can manually add the details to /etc/wpa_supplicant/wpa_supplicant.conf if you know them.
This option will allow you to scan for local WiFi networks and update the Pi. If you then reboot or use the Force... option ,see below, then it will connect to the new WiFi network.
This option only works for WiFi networks where only a password is required. 

### Force to a Hotspot or Force to Network if SSID in Range
This option is only for the Autohotspot setups.
If you are at home and connected to your home network but would like to use the hotspot. This option will force the pi to hotspot mode and will ignore your home network until the next reboot. If you use this option again while in hotspot mode it will attempt to connect to a known network. This will go back to the hotspot if no valid WiFi network is found or there is a connection issue.

### Change the Hotspots SSID and Password
By default the hotspot ssid is RPiHotSpot with a password of 1234567890. Use this option to change either or both SSID and Password.
You will be prompted to change both but if you make no entry and press enter the existing setting will be kept.
The password must be at least 8 characters.

### Credits to the awesome AutoHotspot project: 
- https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/183-raspberry-pi-automatic-hotspot-and-static-hotspot-installer
- https://github.com/RaspberryConnect/AutoHotspot-Installer