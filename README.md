### Function Descriptions
`download_password_list(url, filename)`: Downloads a password list from the provided URL if it is not already present in the specified filename.

`check_connection(target_ssid)`: Verifies if the WiFi is connected and authenticated to the target SSID.

`confirm_internet_access()`: Checks for internet connectivity by attempting to reach Google.

`brute_force_wifi(target_ssid, password_file)`: Tries each password from the file to connect to the target SSID until successful.

### Important Notes
Usage of the Script: This script should only be used for testing on networks you have permission to access.

Password List Requirements: The script assumes the passwords are between 8 and 63 characters, as per WPA2 requirements.

### Legal Disclaimer: 
**Unauthorized** access to networks is **illegal**. Use this script responsibly and only on networks where you have explicit permission to attempt access.


### Example usage inside file or outside(change code)

```

if __name__ == "__main__":
    target_ssid = "SSID_NAME_LIKE_SWEET_HOME_OR_SOMETHING"
    password_file = "passwords.txt"
    download_password_list("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords-100000.txt", password_file)
    brute_force_wifi(target_ssid, password_file)
```
