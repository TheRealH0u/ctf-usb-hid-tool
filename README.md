- [ctf-usb-hid-tool](#ctf-usb-hid-tool)
  - [Usage](#usage)
  - [Auto extract keys](#auto-extract-keys)
  - [To do](#to-do)

# ctf-usb-hid-tool

This project was made because there was no other tool that would give me the right solution to an ECSC ctf challenge.
The challenge in mind can be found inside [tests](https://github.com/TheRealH0u/ctf-usb-hid-tool/tests) folder.

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

## To do
- [ ] Add bsnoop compatibility
- [ ] Add more scan codes (INSERT, PAGE UP, PAGE DN, etc.)