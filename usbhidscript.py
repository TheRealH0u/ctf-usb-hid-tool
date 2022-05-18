import sys
import subprocess

lcasekey = {}
ucasekey = {}

lcasekey[4] = "a"
ucasekey[4] = "A"
lcasekey[5] = "b"
ucasekey[5] = "B"
lcasekey[6] = "c"
ucasekey[6] = "C"
lcasekey[7] = "d"
ucasekey[7] = "D"
lcasekey[8] = "e"
ucasekey[8] = "E"
lcasekey[9] = "f"
ucasekey[9] = "F"
lcasekey[10] = "g"
ucasekey[10] = "G"
lcasekey[11] = "h"
ucasekey[11] = "H"
lcasekey[12] = "i"
ucasekey[12] = "I"
lcasekey[13] = "j"
ucasekey[13] = "J"
lcasekey[14] = "k"
ucasekey[14] = "K"
lcasekey[15] = "l"
ucasekey[15] = "L"
lcasekey[16] = "m"
ucasekey[16] = "M"
lcasekey[17] = "n"
ucasekey[17] = "N"
lcasekey[18] = "o"
ucasekey[18] = "O"
lcasekey[19] = "p"
ucasekey[19] = "P"
lcasekey[20] = "q"
ucasekey[20] = "Q"
lcasekey[21] = "r"
ucasekey[21] = "R"
lcasekey[22] = "s"
ucasekey[22] = "S"
lcasekey[23] = "t"
ucasekey[23] = "T"
lcasekey[24] = "u"
ucasekey[24] = "U"
lcasekey[25] = "v"
ucasekey[25] = "V"
lcasekey[26] = "w"
ucasekey[26] = "W"
lcasekey[27] = "x"
ucasekey[27] = "X"
lcasekey[28] = "y"
ucasekey[28] = "Y"
lcasekey[29] = "z"
ucasekey[29] = "Z"
lcasekey[30] = "1"
ucasekey[30] = "!"
lcasekey[31] = "2"
ucasekey[31] = "@"
lcasekey[32] = "3"
ucasekey[32] = "#"
lcasekey[33] = "4"
ucasekey[33] = "$"
lcasekey[34] = "5"
ucasekey[34] = "%"
lcasekey[35] = "6"
ucasekey[35] = "^"
lcasekey[36] = "7"
ucasekey[36] = "&"
lcasekey[37] = "8"
ucasekey[37] = "*"
lcasekey[38] = "9"
ucasekey[38] = "("
lcasekey[39] = "0"
ucasekey[39] = ")"
lcasekey[40] = "Enter"
ucasekey[40] = "Enter"
lcasekey[41] = "<esc>"
ucasekey[41] = "<esc>"
lcasekey[42] = "backspace"
ucasekey[42] = "backspace"
lcasekey[43] = "tab"
ucasekey[43] = "tab"
lcasekey[44] = "space"
ucasekey[44] = "space"
lcasekey[45] = "-"
ucasekey[45] = "_"
lcasekey[46] = "="
ucasekey[46] = "+"
lcasekey[47] = "["
ucasekey[47] = "{"
lcasekey[48] = "]"
ucasekey[48] = "}"
lcasekey[49] = "\\"
ucasekey[49] = "|"
lcasekey[50] = " "
ucasekey[50] = " "
lcasekey[51] = ";"
ucasekey[51] = ":"
lcasekey[52] = "'"
ucasekey[52] = "\""
lcasekey[53] = "`"
ucasekey[53] = "~"
lcasekey[54] = ","
ucasekey[54] = "<"
lcasekey[55] = "."
ucasekey[55] = ">"
lcasekey[56] = "/"
ucasekey[56] = "?"
lcasekey[57] = "CapsLock"
ucasekey[57] = "CapsLock"

ucasekey[74] = "home"
lcasekey[74] = "home"

ucasekey[76] = "del"
lcasekey[76] = "del"

ucasekey[77] = "end"
lcasekey[77] = "end"

lcasekey[79] = "Right"
ucasekey[79] = "Right"
lcasekey[80] = "Left"
ucasekey[80] = "Left"
lcasekey[81] = "Down"
ucasekey[81] = "Down"
lcasekey[82] = "Up"
ucasekey[82] = "Up"

lcasekey[84] = "/"
ucasekey[84] = "/"
lcasekey[85] = "*"
ucasekey[85] = "*"
lcasekey[86] = "-"
ucasekey[86] = "-"
lcasekey[87] = "+"
ucasekey[87] = "+"
lcasekey[88] = "Enter"
ucasekey[88] = "Enter"
lcasekey[89] = "1"
ucasekey[89] = "1"
lcasekey[90] = "2"
ucasekey[90] = "2"
lcasekey[91] = "3"
ucasekey[91] = "3"
lcasekey[92] = "4"
ucasekey[92] = "4"
lcasekey[93] = "5"
ucasekey[93] = "5"
lcasekey[94] = "6"
ucasekey[94] = "6"
lcasekey[95] = "7"
ucasekey[95] = "7"
lcasekey[96] = "8"
ucasekey[96] = "8"
lcasekey[97] = "9"
ucasekey[97] = "9"
lcasekey[98] = "0"
ucasekey[98] = "0"
lcasekey[99] = "."
ucasekey[99] = "."

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
