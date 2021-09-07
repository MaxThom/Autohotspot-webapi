import hotspot.constants as constants


def read_networks_in_wpa_supplicant(in_lines):
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
  return networks, out_lines
    
def update_add_network(networks, new_ssid):
  isFound = False
  for network in networks:
    if network["ssid"] == f"\"{new_ssid['ssid']}\"":
      network["psk"] = f"\"{new_ssid['psk']}\""
      isFound = True
      break
  if not isFound:
    networks.append({
      'ssid': f"\"{new_ssid['ssid']}\"",
      'psk': f"\"{new_ssid['psk']}\"",
      'key_mgmt': "WPA-PSK"
    })
  return networks

def generate_wpa_supplicant(networks, out_lines):
  for network in networks:
    out_lines.append("network={\n")
    for key, value in network.items():
      out_lines.append(f"    {key}={value}\n")      
    out_lines.append("}\n\n")
  return out_lines

def execute_script(command):  
  process = subprocess.Popen([f"sudo /bin/bash {command}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
  result, err = process.communicate()  
  print(result)
  print(err)
  return result, err