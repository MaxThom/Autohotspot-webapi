
from flask import Blueprint, request, jsonify, render_template
import hotspot.constants as constants
import subprocess

hotspot_bp = Blueprint('hotspot', __name__)


@hotspot_bp.route('/')
def get():
    hotspot = {'status': 'WIFI'}
    return render_template('hotspot.html',hotspot=hotspot)

@hotspot_bp.route('/api/hotspot', methods=['GET'])
def api_get():
    data = request.get_json()
    print(data)
    print(data["command"])
    print(data["ssid"])
    print(data["psk"])
    
    commandAction[data["command"]](data)
    
    return jsonify(request.get_json())


### https://geekflare.com/python-run-bash/
def command_add_wifi(json):
  print("-> Adding wifi")
  
  # Read file
  # If one ssid equal the input, change the password
  # Else add a new one

  networks = []
  with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as f:
    in_lines = f.readlines()  

  print(in_lines)

  # Discover networks
  out_lines = []
  networks = []
  i = 0
  isInside = False
  for line in in_lines:
    if "network={" == line.strip().replace(" ", ""):
      networks.append({})
      isInside = True
    elif "}" == line.strip().replace(" ", ""):
      i += 1
      isInside = False
    elif isInside:      
      key_value = line.strip().split("=")
      networks[i][key_value[0]] = key_value[1]
    else:
      out_lines.append(line)

  # Update password or create new
  isFound = False
  for network in networks:
    if network["ssid"] == f"\"{json['ssid']}\"":
      network["psk"] = f"\"{json['psk']}\""
      isFound = True
      break
  if not isFound:
    networks.append({
      'ssid': f"\"{json['ssid']}\"",
      'psk': f"\"{json['psk']}\"",
      'key_mgmt': "WPA-PSK"
    })

  # Generate file
  for network in networks:
    out_lines.append("network={\n")
    for key, value in network.items():
      out_lines.append(f"    {key}={value}\n")      
    out_lines.append("}\n\n")

  # Write to files
  with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
    for line in out_lines:
      f.write(line)


  #for network in networks:
  #  print(network)
  print(out_lines)

  for line in out_lines:
    print(line)
    

  print("-> Wifi added !")
  

def command_hotspot_ssid(json):
  print("-> Setting hotspot ssid and password")
  command = f"sudo /bin/bash ./hotspot/Autohotspot/hotspot_ssid.sh {json['ssid']} {json['psk']}"
  print(command)
  process = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
  result, err = process.communicate()
  
  print(err)
  print(result)

  print("-> Hotspot ssid and password set")

def command_force(json):
  print("-> Forcing hotspot or wifi")

  process = subprocess.Popen(["sudo /bin/bash ./hotspot/Autohotspot/force_hotspot_wifi.sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
  result, err = process.communicate()
  print(err)
  print(result)

  print("-> Hotspot or wifi forced")

def command_install_ahs_eth(json):
  print("-> Installing Auto Hotspot with internet")

def command_install_ahs_no_eth(json):
  print("-> Installing Auto Hotspot without internet")

def command_install_hs_eth(json):
  print("-> Installing permanent hotspot with internet")

def command_uninstall_ahs(json):
  print("-> Uninstalling Auto Hostspot")

commandAction = {
      constants.COMMAND_ADD_WIFI: command_add_wifi,
      constants.COMMAND_HOTSPOT_SSID: command_hotspot_ssid,
      constants.COMMAND_FORCE: command_force,
      constants.COMMAND_INSTALL_AHS_ETH: command_install_ahs_eth,
      constants.COMMAND_INSTALL_AHS_NO_ETH: command_install_ahs_no_eth,
      constants.COMMAND_INSTALL_HS_ETH: command_install_hs_eth,
      constants.COMMAND_UNINSTALL_AHS: command_uninstall_ahs,
  }