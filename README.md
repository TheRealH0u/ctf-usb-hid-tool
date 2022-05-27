- [ctf-usb-hid-tool](#ctf-usb-hid-tool)
  - [Usage](#usage)
  - [Auto extract keys](#auto-extract-keys)
  - [Updates](#updates)
    - [1.2](#12)
  - [To do](#to-do)

# ctf-usb-hid-tool

This project was made because there was no other tool that would give me the right solution to an ECSC ctf challenge.
The challenge in mind can be found inside [tests](/tests) folder.

## Usage
```bash
python3 usb-hid-script.py [filename/.pcapng/.pcap]
```  

## Auto extract keys
For now only `.pcap` and `.pcapng` are whitelisted files that can be used with the script.
That's because the script automatically extracts the keys from the pcap file.
```python
extractedKeys = subprocess.check_output("tshark -r "+sys.argv[1]+" -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2'", shell=True)
```
## Updates
### 1.2
- Removed my custom code for flags/arguments/errors/help and started using argparse
- Split up main and debug into seperate functions an subparsers
- Added more USB HDI keys
- Added all of the USB HDI keys into respectful dictionaries (errors, keys, numpad, modmask)
- Other things that I honestly can't remember

## To do
- [x] ~~Add bsnoop compatibility~~
- [x] ~~Add more scan codes (INSERT, PAGE UP, PAGE DN, etc.)~~
- [x] ~~Change how lovercase and uppercase key codes are stored~~
- [ ] Check if tests work
- [ ] Add CTRL function like CTRL + C/V/A/X
- [ ] Add different keymaps other than US
  - [ ] Add a flag for the different keymaps
  - [ ] Figure out how to store all the keymaps
- [ ] Make it a whole program/tool (/bin/bash)
