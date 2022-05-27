import sys
import subprocess
from pathlib import Path
import argparse

"""
Modifier masks - used for the first byte in the HID report.
NOTE: The second byte in the report is reserved, it's always 0x00
"""
MODMASK = {
	"01" : "LCTRL",
	"02" : "LSHIFT",
	"04" : "LALT",
	"08" : "LMETA",
	"10" : "RCTRL",
	"20" : "RSHIFT",
	"40" : "RALT",
	"80" : "RMETA"
}

"""
Key codes for errors
"""
HIDERRORS = {
	"00" : "none",
	"01" : "Keyboard Error Roll Over", # NOTE: Used for all slots if too many keys are pressed
	"02" : "Keyboard POST Fail",
	"03": "Keyboard Error Undefined"
}

"""
Keys on the keyboard
"""
KEY = {
	"04" : ["a", "A"],
	"05" : ["b", "B"],
	"06" : ["c", "C"],
	"07" : ["d", "D"],
	"08" : ["e", "E"],
	"09" : ["f", "F"],
	"0a" : ["g", "G"],
	"0b" : ["h", "H"],
	"0c" : ["i", "I"],
	"0d" : ["j", "J"],
	"0e" : ["k", "K"],
	"0f" : ["l", "L"],
	"10" : ["m", "M"],
	"11" : ["n", "N"],
	"12" : ["o", "O"],
	"13" : ["p", "P"],
	"14" : ["q", "Q"],
	"15" : ["r", "R"],
	"16" : ["s", "S"],
	"17" : ["t", "T"],
	"18" : ["u", "U"],
	"19" : ["v", "V"],
	"1a" : ["w", "W"],
	"1b" : ["x", "X"],
	"1c" : ["y", "Y"],
	"1d" : ["z", "Z"],
	"1e" : ["1", "!"],
	"1f" : ["2", "@"],
	"20" : ["3", "#"],
	"21" : ["4", "$"],
	"22" : ["5", "%"],
	"23" : ["6", "^"],
	"24" : ["7", "&"],
	"25" : ["8", "*"],
	"26" : ["9", "("],
	"27" : ["0", ")"],
	"28" : ["enter", "enter"],
	"29" : ["<esc>", "<esc>"],
	"2a" : ["backspace", "backspace"],
	"2b" : ["tab", "tab"],
	"2c" : ["spacebar", "spacebar"],
	"2d" : ["-", "_"],
	"2e" : ["=", "+"],
	"2f" : ["[", "{"],
	"30" : ["]", "}"],
	"31" : ["\\", "|"],
	"32" : ["#", "~"],
	"33" : [";", ":"],
	"34" : ["'", "\""],
	"35" : ["`", "~"],
	"36" : [",", "<"],
	"37" : [".", ">"],
	"38" : ["/", "?"],
	"39" : ["caps", "caps"],
	"3a" : ["f1", "f1"],
	"3b" : ["f2", "f2"],
	"3c" : ["f3", "f3"],
	"3d" : ["f4", "f4"],
	"3e" : ["f5", "f5"],
	"3f" : ["f6", "f6"],
	"40" : ["f7", "f7"],
	"41" : ["f8", "f8"],
	"42" : ["f9", "f9"],
	"43" : ["f10", "f10"],
	"44" : ["f11", "f11"],
	"45" : ["f12", "f12"],
	"46" : ["print", "print"],
	"47" : ["scrollLock", "scrollLock"],
	"48" : ["pause", "pause"],
	"49" : ["insert", "insert"],
	"4a" : ["home", "home"],
	"4b" : ["pageUp", "pageUp"],
	"4c" : ["delete", "delete"],
	"4d" : ["end", "end"],
	"4e" : ["pageDown", "pageDown"],
	"4f" : ["right", "right"],
	"50" : ["left", "left"],
	"51" : ["down", "down"],
	"52" : ["up", "up"]
}

"""
Numpad keys
"""
NUMPAD = {
	"53" : ["numLock", "numLock"],
	"54" : ["/", "/"],
	"55" : ["*", "*"],
	"56" : ["-", "-"],
	"57" : ["+", "+"],
	"58" : ["enter", "enter"],
	"59" : ["1", "end"],
	"5a" : ["2", "down"],
	"5b" : ["3", "pageDn"],
	"5c" : ["4", "left"],
	"5d" : ["5", "5"],
	"5e" : ["6", "right"],
	"5f" : ["7", "home"],
	"60" : ["8", "up"],
	"61" : ["9", "pageUp"],
	"62" : ["0", "insert"],
	"63" : [".", "delete"]
}

# Predefine variables that are gonna be used
outString = [""]
position = 0
oSline = 0 #Short for outStringline

def USBHIDFunction(data: str):
	"""
	Functions to transcribe from USB HID to readable string
	"""
	
	global outString
	global oSline
	global position

	if data == "enter" or data == "tab":
		outString.append("")
		oSline += 1
	elif data == "space":
		outString[oSline] += " "
	elif data == "left":
		position -= 1
	elif data == "right":
		position += 1
	elif data == "up":
		oSline -= 1
	elif data == "down":
		oSline += 1
	elif data == "delete":
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

def run(args):
	# pcapng/pcap extraction
	if args.file.endswith(".pcapng") or args.file.endswith(".pcap"):
		extractedKeys = subprocess.check_output("tshark -r "+args.file+" -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2'", shell=True) 
		extractedKeys = extractedKeys.decode("utf-8")
		extractedKeys = extractedKeys.splitlines()

	# bsnoop extraction
	elif args.file.endswith(".bsnoop"):
		extractedKeys = subprocess.check_output("tshark -r "+args.file+" -Y 'btatt.opcode == 0x1b && btatt.handle == 0x002c && btatt.value != 00:00:00:00:00:00:00' -T fields -e btatt.value | sed 's/.*:00/00:&/'")
		extractedKeys = extractedKeys.decode("utf-8")
		extractedKeys = extractedKeys.splitlines()

	# other files where hex values can be extracted
	else:
		with open(args.file, "r") as f:
			lines = f.readlines()
			extractedKeys = []
			for line in lines:
				if line != "\n":
					extractedKeys.append(line)


	count = {}
	
	for line in extractedKeys:

		line = line.split(":")

		try:
			# NOTE: Bytes from 2 - 7 are keys pressed.
			# We check if the user stopped pressing multiple keys together
			if line[3] == "00":

				#LCTRL and RCTRL
				if line[0] == "01" or line[0] == "10":
					# TODO: Add CTRL functions like CTRL + C/V/A/X
					print("CTRL+"+KEY[line[2]][0])

				#LSHIFT, RSHIFT and RALT
				elif line[0] == "02" or line[0] == "20" or line[0] == "40":
					USBHIDFunction(KEY[line[2]][1])

				else:
					USBHIDFunction(KEY[line[2]][0])

		except Exception as e:
			if args.count_errors:
				try:
					count[HIDERRORS[line[2]]] = count[HIDERRORS[line[2]]] + 1

				except:
					count[HIDERRORS[line[2]]] = 1

	# * Output section of the program
	if args.line_number:
		for s in range(0, len(outString)):
			print(s+1,":",outString[s])
	else:
		for s in outString:
			print(s)

	if args.count_errors:
		print("-"*10+"ERRORS"+"-"*10)
		for k,v in count.items():
			print("{:25s} : {:5d}".format(k,v))

def debug(args):
	# pcapng/pcap extraction
	if args.file.endswith(".pcapng") or args.file.endswith(".pcap"):
		extractedKeys = subprocess.check_output("tshark -r "+args.file+" -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2'", shell=True) 
		extractedKeys = extractedKeys.decode("utf-8")
		extractedKeys = extractedKeys.splitlines()

	# bsnoop extraction
	elif args.file.endswith(".bsnoop"):
		extractedKeys = subprocess.check_output("tshark -r "+args.file+" -Y 'btatt.opcode == 0x1b && btatt.handle == 0x002c && btatt.value != 00:00:00:00:00:00:00' -T fields -e btatt.value | sed 's/.*:00/00:&/'")
		extractedKeys = extractedKeys.decode("utf-8")
		extractedKeys = extractedKeys.splitlines()

	# other files where hex values can be extracted
	else:
		with open(args.file, "r") as f:
			lines = f.readlines()
			extractedKeys = []
			for line in lines:
				if line != "\n":
					extractedKeys.append(line)
	
	for line in extractedKeys:

		line = line.split(":")

		# NOTE: Bytes from 2 - 7 are keys pressed.
		# We check if the user stopped pressing multiple keys together
		if line[3] == "00":

			#LCTRL and RCTRL
			if line[0] == "01" or line[0] == "10":
				# TODO: Add CTRL functions like CTRL + C/V/A/X
				if line[2] in KEY:
					print("CTRL+"+KEY[line[2]][0])
				elif line[2] in NUMPAD:
					print("CTRL+"+NUMPAD[line[2][0]])
				elif line[2] in HIDERRORS:
					print(HIDERRORS[line[2]])

			#LSHIFT, RSHIFT and RALT
			elif line[0] == "02" or line[0] == "20" or line[0] == "40":
				if line[2] in KEY:
					print(KEY[line[2]][1])
				elif line[2] in NUMPAD:
					print(NUMPAD[line[2]][1])
				elif line[2] in HIDERRORS:
					print(HIDERRORS[line[2]])

			else:
				if line[2] in KEY:
					print(KEY[line[2]][0])
				elif line[2] in NUMPAD:
					print(NUMPAD[line[2]][0])
				elif line[2] in HIDERRORS:
					print(HIDERRORS[line[2]])

def is_valid_file(parser, arg):
	# Checks if a file exists
    if not Path(arg).is_file():
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='script to decode USB HDI Keyboard scan codes to string')
	
	subparsers = parser.add_subparsers(dest="group")

	# All the other commands

	mainCommandsParser = subparsers.add_parser("run", help="Run normal commands")
	mainCommandsParser.add_argument("file", metavar="FILE", type=lambda x: is_valid_file(parser, x), help="File to be decoded")
	mainCommandsParser.add_argument("-n", "--line-number", help="print line number with output lines", action="store_true")
	mainCommandsParser.add_argument("-e", "--count-errors", action="store_true", help="print number of errors")
	
	# Debug command

	debugParser = subparsers.add_parser("debug", help="Used to debug the output of the file")
	debugParser.add_argument("file", metavar="FILE", type=lambda x: is_valid_file(parser, x), help="File to be debugged")
	
	args = parser.parse_args()
	if args.group == "debug":
		debug(args)
	elif args.group == "run":
		run(args)