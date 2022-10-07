import sys
import subprocess

KEY_CODES = {
    4: ['a', 'A'],
    5: ['b', 'B'],
    6: ['c', 'C'],
    7: ['d', 'D'],
    8: ['e', 'E'],
    9: ['f', 'F'],
    10: ['g', 'G'],
    11: ['h', 'H'],
    12: ['i', 'I'],
    13: ['j', 'J'],
    14: ['k', 'K'],
    15: ['l', 'L'],
    16: ['m', 'M'],
    17: ['n', 'N'],
    18: ['o', 'O'],
    19: ['p', 'P'],
    20: ['q', 'Q'],
    21: ['r', 'R'],
    22: ['s', 'S'],
    23: ['t', 'T'],
    24: ['u', 'U'],
    25: ['v', 'V'],
    26: ['w', 'W'],
    27: ['x', 'X'],
    28: ['y', 'Y'],
    29: ['z', 'Z'],
    30: ['1', '!'],
    31: ['2', '@'],
    32: ['3', '#'],
    33: ['4', '$'],
    34: ['5', '%'],
    35: ['6', '^'],
    36: ['7', '&'],
    37: ['8', '*'],
    38: ['9', '('],
    39: ['0', ')'],
    40: ['Enter', 'Enter'],
    41: ['<esc>', '<esc>'],
    42: ['backspace', 'backspace'],
    43: ['tab', 'tab'],
    44: ['space', 'space'],
    45: ['-', '_'],
    46: ['=', '+'],
    47: ['[', '{'],
    48: [']', '}'],
    49: ['\\', '|'],
    50: [' ', ' '],
    51: [';', ':'],
    52: ["'", '"'],
    53: ['`', '~'],
    54: [',', '<'],
    55: ['.', '>'],
    56: ['/', '?'],
    57: ['CapsLock', 'CapsLock'],
    74: ['home', 'home'],
    76: ['del', 'del'],
    77: ['end', 'end'],
    79: ['Right', 'Right'],
    80: ['Left', 'Left'],
    81: ['Down', 'Down'],
    82: ['Up', 'Up'],
    84: ['/', '/'],
    85: ['*', '*'],
    86: ['-', '-'],
    87: ['+', '+'],
    88: ['Enter', 'Enter'],
    89: ['1', '1'],
    90: ['2', '2'],
    91: ['3', '3'],
    92: ['4', '4'],
    93: ['5', '5'],
    94: ['6', '6'],
    95: ['7', '7'],
    96: ['8', '8'],
    97: ['9', '9'],
    98: ['0', '0'],
    99: ['.', '.'],
}

# Predefined variables
# ------
output = [""] # output
holdingShift = False # Variable for KeyboardMove()
position_x_shift = 0 # Position of cursor while highlighting
position_x = 0 # Position of cursor
position_y = 0 # Position of line
copyText = ""
# ------

# Keyboard functions
def KeyboardMove(data, shift=False):
	global holdingShift
	global position_x
	global position_y
	global position_x_shift

	if data == "Left":
		if shift and not holdingShift:
			position_x_shift = position_x # If were holding shift we take the current position so we know how many character we highlighted.
			holdingShift = True # If were still holding shift, we musnt overwrite the previous position shift, thats why we make a variable hodling shift to account for that
			position_x -= 1
		elif not shift and holdingShift:
			holdingShift = False # If were not holding shift were not holding shift
			if position_x > position_x_shift: # If we highlight to the right and the press left we go back to the previous position on position_x_shift
				position_x = position_x_shift 
			# If we press left when we highlighted to the left we just leave the position_x as it is
		else:
			position_x -= 1
	elif data == "Right":
		if shift and not holdingShift:
			position_x_shift = position_x
			holdingShift = True
			position_x += 1
		elif not shift and holdingShift:
			holdingShift = False
			if position_x < position_x_shift: # Same here. If we highlight to the left and press right we go back to the highlighting position
				position_x = position_x_shift
			# On the other hand we go to the position that is position_x
		else:
			position_x += 1
	elif data == "Up":
		""" TODO: 
		Support for multi line highlighting with up and down
		"""
		
		position_y -= 1
	elif data == "Down":
		position_y += 1
def KeyboardCopyPaste(data):
	global position_x
	global position_y
	global position_x_shift
	global copyText
	global output

	if data == "c":
		copyText = output[position_y]
		if position_x > position_x_shift:
			copyText = copyText[position_x_shift:position_x]
		else:
			copyText = copyText[position_x:position_x_shift]
	elif data == "v":
		txtLeft, txtRight = output[position_y][:position_x],output[position_y][position_x:]
		txtLeft += copyText
		output[position_y] = txtLeft + txtRight
		position_x += len(copyText)
def KeyboardPrint(data):
	global output
	global position_y
	global position_x 
		
	if data == "Enter" or data == "tab":
		output.append("")
		position_y += 1
		position_x = 0
	elif data == "space":
		txtLeft, txtRight = output[position_y][:position_x],output[position_y][position_x:]
		txtLeft += " "
		output[position_y] = txtLeft + txtRight
		position_x += 1
	elif data == "del":
		txtLeft, txtRight = output[position_y][:position_x],output[position_y][position_x:]
		txtRight = txtRight[1:]
		output[position_y] = txtLeft + txtRight
	elif data == "backspace":
		txtLeft, txtRight = output[position_y][:position_x],output[position_y][position_x:]
		txtLeft = txtLeft[:-1]
		output[position_y] = txtLeft + txtRight
		position_x -= 1
	elif data == "home":
		position_x = 0
	elif data == "end":
		position_x = len(output[position_y])
	else:
		txtLeft, txtRight = output[position_y][:position_x],output[position_y][position_x:]
		txtLeft += data
		output[position_y] = txtLeft + txtRight
		position_x += 1
		


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
		if hexKey in KEY_CODES:
			if line[3] == "00":

				# LCTRL and RCTRL modifier
				if line[0] == "01" or line[0] == "10":
					KeyboardCopyPaste(KEY_CODES[hexKey][0])

				#LSHIFT, RSHIFT and RALT modifiers
				elif line[0] == "02" or line[0] == "20" or line[0] == "40":
					if KEY_CODES[hexKey][0] in ["Up","Down","Left","Right"]:
						KeyboardMove(KEY_CODES[hexKey][0], True)
					else:
						KeyboardPrint(KEY_CODES[hexKey][1])
				else:
					if KEY_CODES[hexKey][0] in ["Up","Down","Left","Right"]:
						KeyboardMove(KEY_CODES[hexKey][0])
					else:
						KeyboardPrint(KEY_CODES[hexKey][0])

	# Print output line by line
	for s in output:
		print(s)
else:
	print("[?] python3 usb-hid-script.py [filename/.pcapng/.pcap]")
