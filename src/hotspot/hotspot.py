
from flask import Blueprint, request, jsonify, render_template
import hotspot.constants as constants
import hotspot.utils as utils
import os.path
import subprocess

hotspot_bp = Blueprint('hotspot', __name__)


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

  if not os.path.exists(constants.WPA_SUPPLICANT):
    return None, f"WAP Supplicant does not exist. Is AutoHostspot installed ? {constants.WPA_SUPPLICANT}"

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
  print("-> Display networks") 

  if not os.path.exists(constants.WPA_SUPPLICANT):
    return None, f"WAP Supplicant does not exist. Is AutoHostspot installed ? {constants.WPA_SUPPLICANT}"

  # Read WPA Supplicant
  with open(constants.WPA_SUPPLICANT, "r") as f:
    in_lines = f.readlines()

  # Discover networks
  networks, out_lines = utils.read_networks_in_wpa_supplicant(in_lines)

  print("-> Networks diplayed !") 
  return networks, None

def command_hotspot_ssid(json):
  print("-> Setting hotspot ssid and password")
  if "ssid" not in json or not json["ssid"]:
    return None, "Missing parameter 'ssid' with string value."
  if "psk" not in json or not json["psk"]:
    return None, "Missing parameter 'psk' with string value."
  if len(json["psk"]) < constants.WIFI_PSK_LENGTH:
    return None, f"Password must be at least {constants.WIFI_PSK_LENGTH} characters."

  os.chmod(constants.AHP_HOTSPOT_SSID_PATH, 0o755)
  result, err = utils.execute_script(f"{constants.AHP_HOTSPOT_SSID_PATH} {json['ssid']} {json['psk']}")
  print("-> Hotspot ssid and password set")
  return result, err

def command_display_hotspot_ssid(json):
  print("-> Display hotspot")
  if not os.path.exists(constants.HOST_APD):
    return None, f"Host APD does not exist. Is AutoHostspot installed ? {constants.HOST_APD}"
  # Read Host APD
  with open(constants.HOST_APD, "r") as f:
    in_lines = f.readlines()

  # Look for ssid and psk
  config = utils.read_ssid_in_hostapd(in_lines)  
   
  print(config)
  print("-> Hotspot displayed !")
  return config, None

def command_force(json):
  print("-> Forcing hotspot or wifi")  
  os.chmod(constants.AHP_FORCE_HS_WIFI_PATH, 0o755)
  result, err = utils.execute_script(f"{constants.AHP_FORCE_HS_WIFI_PATH}")
  print("-> Hotspot or wifi forced")
  return result, err

def command_display_current_network(json):
  print("-> Display current network")  
  result = subprocess.run(["iwgetid"], capture_output=True, text=True)
  print("stdout:", result.stdout)
  print("stderr:", result.stderr)

  iw = ""
  if not result.stdout:
    iw = "hotspot"
  else:
    iw = result.stdout.split(":")[1].strip().replace("\n", "").replace("\"", "")

  print("-> Current network displayed !")
  return iw, result.stderr

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
    constants.COMMAND_DISPLAY_HOTSPOT_SSID: command_display_hotspot_ssid,
    constants.COMMAND_FORCE: command_force,
    constants.COMMAND_DISPLAY_CURRENT_NETWORK: command_display_current_network,
    constants.COMMAND_INSTALL_AHS_ETH: command_install_ahs_eth,
    constants.COMMAND_INSTALL_AHS_NO_ETH: command_install_ahs_no_eth,
    constants.COMMAND_INSTALL_HS_ETH: command_install_hs_eth,
    constants.COMMAND_UNINSTALL_AHS: command_uninstall_ahs,
}
