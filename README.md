# Project Spectrum
The goal of this project is to connect a rpi with many led matrices and diplay animations.
It is controllable via wifi connection using a phone or computer. 
The project has a hotspot feature, if the device is out of range of known networks, it will automaticly create a hotspot.
The wifi and hotspot settings can be configured via the api.
Enjoy :)

# Documentation
1. [Hotspot API](\docs\hotspot_api.md)

# Motivation
The motivation behind this project is too decorate our homes, parties, events, etc.
Moreover, the second goal is too learn how to make an electronics, how to use wifi, hotspot, complex animations and more.

# Technologies

### RPI
The web server (flask) and ledstrip connection on the rpi are made with Python3.

##### Hardware
 - Raspberry pi 4B
 - WS2812B Led matrice x 9
 - Electric cables
 - Power supply

# Features
- Being able to control the device using a phone or computer and without internet connection
- Being plug and play as much as possible
- User will be able to select a bunch of animations
- User will be able to create an animation playlist with loop or not
- User will be able to divide the matrice in different section and target those sections individually with animations

# How to use
#### **Commands for Systemd**
 - sudo nano /lib/systemd/system/spectrum.service 
 - sudo chmod +x /lib/systemd/system/spectrum.service
 - sudo systemctl daemon-reload
 - sudo systemctl enable spectrum.service
 - sudo systemctl status spectrum.service

#### **Command for Cronjobs**
 - sudo crontab -e
 - sudo crontab -l

# Installation
 #### Rpi
 1. Enable SSH, VNC and SPI in interfaces configuration
 2. Install AutoHotspot
 3. Install Git, Python and Pip :
    - sudo apt install git
    - sudo apt install python3
    - sudo apt-get install python3-pip
 5. Download repo
 6. Install requirements : sudo pip3 install -r requirements.txt
 7. Add Spectrum-Update script to crontab
    - Open terminal and type : sudo crontab -e
    - Add this line to start server update check on system boot : **@reboot sh /home/pi/Desktop/Spectrum-rpi/Spectrum-Update.sh >/home/pi/Desktop/Spectrum-rpi/Logs/cronlogs 2>&1**
    - Save, you can confirm using sudo crontab -l
 8. Add Systemd unit file to systemd deamon
    - sudo cp Spectrum.service /lib/systemd/system/
    - sudo chmod +x /lib/systemd/system/Spectrum.service
    - sudo systemctl daemon-reload
    - sudo systemctl enable Spectrum.service
    - sudo systemctl status Spectrum.service
 9. Reboot
    - sudo reboot

# Credits
- The awesome AutoHotspot: 
    - https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/183-raspberry-pi-automatic-hotspot-and-static-hotspot-installer
    - https://github.com/RaspberryConnect/AutoHotspot-Installer
- The great rpi-ws281x library
    - https://github.com/rpi-ws281x/rpi-ws281x-python
- Thanks to RaspberryPi for their awesome devices
    - https://www.raspberrypi.org/

# Liscense
MIT

# RoadMap
*September 2021*
- [x] - Create Hotspot and Wifi feature
- [ ] - IMU Integration
- [ ] - Create the device with the rpi, wires, led matrices and power supply
- [ ] - Control the leds using python
- [ ] - Configure Raspbian to autolaunch the script on bootup
- [ ] - Auto update the server from git
- [ ] - Create a phone app using Xamarin and learn the basics
- [ ] - Add handshake when initializing connections to discover servers capabilities (animations, etc)
- [ ] - Create a dynamic UI for animations
- [ ] - Create playlist for animations
- [ ] - Create segments on the leds for animations to target those sections
- [ ] - Add more animations
- [ ] - Add different ledstrip type (SK6812)


