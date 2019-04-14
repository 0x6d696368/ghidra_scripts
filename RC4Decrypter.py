#RC4 decrypts the selected memory with a user input key.
#
#@author 
#@category Memory
#@keybinding 
#@menupath Tools.Decoders.RC4 Decrypter
#@toolbar 

import array

from subprocess import Popen, PIPE
from ghidra.program.model.listing import CodeUnit
from ghidra.program.util import ProgramSelection
from ghidra.util.exception import CancelledException
from ghidra.program.model.mem import MemoryAccessException


SCRIPT_NAME="RC4Decrypter.py"
COMMENT_STYLE = CodeUnit.PLATE_COMMENT

try:
	key = askBytes(SCRIPT_NAME, "RC4 Key")
except CancelledException as e:
	print "[!] CANCELLED: " + str(e)
	exit()

if currentSelection == None or currentSelection.isEmpty():
	print "[!] FAILED: please make a selection"
	exit()

set = currentSelection

ranges = set.getAddressRanges(True)

for r in ranges:
	begin = r.getMinAddress()
	end = r.getMaxAddress()
	length = r.getLength()

	status = "Processing selection: " + r.toString()
	print "[+] " + status

	try:
		bytes = getBytes(begin,length)
	except MemoryAccessException as e:
		print "[!] FAILED: " + str(e)
		continue

	if r.getLength() > PIPE_BUFFER_SIZE:
		print "[!] ERROR: Selection larger than the pipe buffer size."
		print "           Either make a smaller selection or increase PIPE_BUFFER_SIZE in the script's source code."
		continue

	def rc4(key, data):
		S = list(range(256))
		j = 0
		
		for i in list(range(256)):
			j = (j + S[i] + key[i % len(key)]) % 256
			S[i], S[j] = S[j], S[i]

		j = 0
		y = 0
		out = array.array('b')

		for i in range(len(data)):
			j = (j + 1) % 256
			y = (y + S[j]) % 256
			S[j], S[y] = S[y], S[j]
			# FIXME: the +128 ... - 128 thing is ugly ... but don't know how else to handle it correctly
			out.append( ( (data[i]+128) ^ S[(S[j] + S[y]) % 256]) - 128 )

		return out
	
	bytes = rc4(key, bytes)

	try:
		setBytes(begin, bytes)
		key_str = "".join('{:02x}'.format(x) for x in key) 
		createBookmark(begin, SCRIPT_NAME, "Key: " + key_str + ", len: " + hex(len(bytes)))
		cu = currentProgram.getListing().getCodeUnitAt(begin)
		if cu == None:
			print "ERROR: CodeUnitAt " + begin.add(addr).toString() + " does not exist! Can't set comment."
			continue
		comment = cu.getComment(COMMENT_STYLE)
		if comment == None or comment == "":
			comment = ""
		else:
			comment += "\n"
		comment += SCRIPT_NAME + "\n"
		comment += "Key: " + key_str + "\n"
		comment += "len: " + hex(len(bytes))
		cu.setComment(COMMENT_STYLE, comment)
		print "[$] SUCCESS"
	except MemoryAccessException as e:
		print "[!] FAILED: " + str(e)
