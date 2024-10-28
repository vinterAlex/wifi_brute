# wifi_brute
sort of brute force based on a txt file with passwords

### Example usage inside file or outside(change code)

```

if __name__ == "__main__":
    target_ssid = "SSID_NAME_LIKE_SWEET_HOME_OR_SOMETHING"
    password_file = "passwords.txt"
    download_password_list("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords-100000.txt", password_file)
    brute_force_wifi(target_ssid, password_file)
```
