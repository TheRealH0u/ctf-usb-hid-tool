import sys
import subprocess

lcasekey = {}
ucasekey = {}

"""
Modifier masks - used for the first byte in the HID report.
NOTE: The second byte in the report is reserved, 0x00
"""
MODMASK = {
	0x01 : "LCTRL",
	0x02 : "LSHIFT",
	0x04 : "LALT",
	0x08 : "LMETA",
	0x10 : "RCTRL",
	0x20 : "RSHIFT",
	0x40 : "RALT",
	0x80 : "RMETA"
}
KEY = {
	0x00 : ["none","none"],
	0x01 : ["[Keyboard Error Roll Over]", "[Keyboard Error Roll Over]"], # NOTE: Used for all slots if too many keys are pressed
	# 0x02 //  Keyboard POST Fail
	# 0x03 //  Keyboard Error Undefined
	0x04 : ["a", "A"],
	0x05 : ["b", "B"],
	0x06 : ["c", "C"],
	0x07 : ["d", "D"],
	0x08 : ["e", "E"],
	0x09 : ["f", "F"],
	0x0a : ["g", "G"],
	0x0b : ["h", "H"],
	0x0c : ["i", "I"],
	0x0d : ["j", "J"],
	0x0e : ["k", "K"],
	0x0f : ["l", "L"],
	0x10 : ["m", "M"],
	0x11 : ["n", "N"],
	0x12 : ["o", "O"],
	0x13 : ["p", "P"],
	0x14 : ["q", "Q"],
	0x15 : ["r", "R"],
	0x16 : ["s", "S"],
	0x17 : ["t", "T"],
	0x18 : ["u", "U"],
	0x19 : ["v", "V"],
	0x1a : ["w", "W"],
	0x1b : ["x", "X"],
	0x1c : ["y", "Y"],
	0x1d : ["z", "Z"],
	0x1e : ["1", "!"],
	0x1f : ["2", "@"],
	0x20 : ["3", "#"],
	0x21 : ["4", "$"],
	0x22 : ["5", "%"],
	0x23 : ["6", "^"],
	0x24 : ["7", "&"],
	0x25 : ["8", "*"],
	0x26 : ["9", "("],
	0x27 : ["0", ")"],
	0x28 : ["enter", "enter"],
	0x29 : ["<esc>", "<esc>"],
	0x2a : ["backspace", "backspace"],
	0x2b : ["tab", "tab"],
	0x2c : ["spacebar", "spacebar"],
	0x2d : ["-", "_"],
	0x2e : ["=", "+"],
	0x2f : ["[", "{"],
	0x30 : ["]", "}"],
	0x31 : ["\\", "|"],
	0x32 : ["#", "~"],
	0x33 : [";", ":"],
	0x34 : ["'", "\""],
	0x35 : ["`", "~"],
	0x36 : [",", "<"],
	0x37 : [".", ">"],
	0x38 : ["/", "?"],
	0x39 : ["caps", "caps"],
	0x3a : ["f1", "f1"],
	0x3b : ["f2", "f2"],
	0x3c : ["f3", "f3"],
	0x3d : ["f4", "f4"],
	0x3e : ["f5", "f5"],
	0x3f : ["f6", "f6"],
	0x40 : ["f7", "f7"],
	0x41 : ["f8", "f8"],
	0x42 : ["f9", "f9"],
	0x43 : ["f10", "f10"],
	0x44 : ["f11", "f11"],
	0x45 : ["f12", "f12"],
	0x46 : ["print", "print"],
	0x47 : ["scrollLock", "scrollLock"],
	0x48 : ["pause", "pause"],
	0x49 : ["insert", "insert"],
	0x4a : ["home", "home"],
	0x4b : ["pageUp", "pageUp"],
	0x4c : ["delete", "delete"],
	0x4d : ["end", "end"],
	0x4e : ["pageDown", "pageDown"],
	0x4f : ["right", "right"],
	0x50 : ["left", "left"],
	0x51 : ["down", "down"],
	0x52 : ["up", "up"]
}
NUMPAD = {
	0x53 : ["numLock", "numLock"],
	0x54 : ["/", "/"],
	0x55 : ["*", "*"],
	0x56 : ["-", "-"],
	0x57 : ["+", "+"],
	0x58 : ["enter", "enter"],
	0x59 : ["1", "end"],
	0x5a : ["2", "down"],
	0x5b : ["3", "pageDn"],
	0x5c : ["4", "left"],
	0x5d : ["5", "5"],
	0x5e : ["6", "right"],
	0x5f : ["7", "home"],
	0x60 : ["8", "up"],
	0x61 : ["9", "pageUp"],
	0x62 : ["0", "insert"],
	0x63 : [".", "delete"]
}

# Predefine variables that are gonna be used
outString = [""]
position = 0
oSline = 0 #Short for outStringline

def isEnter(data):
	if ucasekey[data] == "Enter":
		return True
	else:
		return False

def USBHIDFunction(data):
	global outString
	global oSline
	global position
	if data == "Enter" or data == "tab":
		outString.append("")
		oSline += 1
	elif data == "space":
		outString[oSline] += " "
	elif data == "Left":
		position -= 1
	elif data == "Right":
		position += 1
	elif data == "Up":
		oSline -= 1
	elif data == "Down":
		oSline += 1
	elif data == "del":
		txtLeft, txtRight = outString[oSline][:len(outString[oSline])+position],outString[oSline][len(outString[oSline])+position:]
		txtRight = txtRight[1:]
		outString[oSline] = txtLeft + txtRight
		position += 1
	elif data == "backspace":
		txtLeft, txtRight = outString[oSline][:len(outString[oSline])+position],outString[oSline][len(outString[oSline])+position:]
		txtLeft = txtLeft[:-1]
		outString[oSline] = txtLeft + txtRight
	elif data == "home":
		position = -len(outString[oSline])
	elif data == "end":
		position = 0
	else:
		txtLeft, txtRight = outString[oSline][:len(outString[oSline])+position],outString[oSline][len(outString[oSline])+position:]
		txtLeft += data
		outString[oSline] = txtLeft + txtRight
		


if (len(sys.argv)) == 2:
	if sys.argv[1].endswith(".pcapng") or sys.argv[1].endswith(".pcap"):
		extractedKeys = subprocess.check_output("tshark -r ./"+sys.argv[1]+" -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2'", shell=True) 
		extractedKeys = extractedKeys.decode("utf-8")
		extractedKeys = extractedKeys.splitlines()
	elif sys.argv[1].endswith(".bsnoop"):
		extractedKeys = subprocess.check_output("tshark -r ./"+sys.argv[1]+" -Y 'btatt.opcode == 0x1b && btatt.handle == 0x002c && btatt.value != 00:00:00:00:00:00:00' -T fields -e btatt.value | sed 's/.*:00/00:&/'")
		extractedKeys = extractedKeys.decode("utf-8")
		extractedKeys = extractedKeys.splitlines()
	else:
		with open(sys.argv[1], "r") as f:
			lines = f.readlines()
			extractedKeys = []
			for line in lines:
				if line != "\n":
					extractedKeys.append(line)
		
		
	for line in extractedKeys:
		line = line.split(":")
		hexKey = int(line[2], 16)
		if hexKey in ucasekey:
			if line[3] == "00":
				#LCTRL and RCTRL
				if line[0] == "01" or line[0] == "10":
					# TO DO
					print("CTRL+"+lcasekey[hexKey])
				#LSHIFT, RSHIFT and RALT
				elif line[0] == "02" or line[0] == "20" or line[0] == "40":
					USBHIDFunction(ucasekey[hexKey])
				else:
					USBHIDFunction(lcasekey[hexKey])
	for s in outString:
		print(s)
else:
	print("[?] python3 usb-hid-script.py [filename/.pcapng/.pcap]")
