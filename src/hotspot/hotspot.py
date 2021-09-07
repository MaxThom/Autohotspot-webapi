
from flask import Blueprint, request, jsonify, render_template
import hotspot.constants as constants
import hotspot.utils as utils
import subprocess

hotspot_bp = Blueprint('hotspot', __name__)


@hotspot_bp.route('/')
def get():
    hotspot = {'status': 'WIFI'}
    return render_template('hotspot.html',hotspot=hotspot)

@hotspot_bp.route('/api/hotspot', methods=['GET'])
def api_get():
  rtn = {}
  try:
    data = request.get_json()
    print(data)    
    rtn["result"], rtn["err"] = commandAction[data["command"]](data)
  except Exception as e: 
    print(e)
    rtn["result"] = None
    rtn["err"] = e

  return jsonify(rtn)

def command_add_wifi(json):
  print("-> Adding wifi")

  if "ssid" not in json or not json["ssid"]:
    return None, "Missing parameter 'ssid' with string value."
  if "psk" not in json or not json["psk"]:
    return None, "Missing parameter 'psk' with string value."
  if len(json["psk"]) < constants.WIFI_PSK_LENGTH:
    return None, f"Password must be at least {constants.WIFI_PSK_LENGTH} characters."

  # Read WPA Supplicant
  with open(constants.WPA_SUPPLICANT, "r") as f:
    in_lines = f.readlines()

  # Discover networks
  networks, out_lines = utils.read_networks_in_wpa_supplicant(in_lines)

  # Update password or add new network
  networks = utils.update_add_network(networks, json)

  # Generate WPA Supplicant
  out_lines = utils.generate_wpa_supplicant(networks, out_lines)

  # Write to files
  with open(constants.WPA_SUPPLICANT, 'w') as f:
    for line in out_lines:
      f.write(line)
   
  print("> wpa_supplicant.conf")
  for line in out_lines:
    print(line)    

  print("-> Wifi added !")
  return networks, None

def command_display_networks(json):
  print("-> Adding wifi") 

  # Read WPA Supplicant
  with open(constants.WPA_SUPPLICANT, "r") as f:
    in_lines = f.readlines()

  # Discover networks
  networks, out_lines = utils.read_networks_in_wpa_supplicant(in_lines)

  return networks, None

def command_hotspot_ssid(json):
  print("-> Setting hotspot ssid and password")
  if "ssid" not in json or not json["ssid"]:
    return None, "Missing parameter 'ssid' with string value."
  if "psk" not in json or not json["psk"]:
    return None, "Missing parameter 'psk' with string value."
  if len(json["psk"]) < constants.WIFI_PSK_LENGTH:
    return None, f"Password must be at least {constants.WIFI_PSK_LENGTH} characters."

  result, err = execute_script(f"{constants.AHP_HOTSPOT_SSID_PATH} {json['ssid']} {json['psk']}")
  print("-> Hotspot ssid and password set")
  return result, err

def command_force(json):
  print("-> Forcing hotspot or wifi")  
  result, err = execute_script(f"{consants.AHP_FORCE_HS_WIFI_PATH}")
  print("-> Hotspot or wifi forced")
  return result, err

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
    constants.COMMAND_DISPLAY_NETWORKS: command_display_networks,
    constants.COMMAND_HOTSPOT_SSID: command_hotspot_ssid,
    constants.COMMAND_FORCE: command_force,
    constants.COMMAND_INSTALL_AHS_ETH: command_install_ahs_eth,
    constants.COMMAND_INSTALL_AHS_NO_ETH: command_install_ahs_no_eth,
    constants.COMMAND_INSTALL_HS_ETH: command_install_hs_eth,
    constants.COMMAND_UNINSTALL_AHS: command_uninstall_ahs,
}
