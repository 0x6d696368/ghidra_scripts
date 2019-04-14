#Pipes the selected memory through a shell process to decode it.
#
# The shell process must:
# - accept the data to be decoded via stdin
# - send decoded output to stdout
# - output error messages to stderr
#@author 
#@category Memory
#@keybinding 
#@menupath Tools.Decoders.Call external (piped) decoder
#@toolbar 

from subprocess import Popen, PIPE
from ghidra.program.model.listing import CodeUnit
from ghidra.program.util import ProgramSelection
from ghidra.util.exception import CancelledException
from ghidra.program.model.mem import MemoryAccessException


PIPE_BUFFER_SIZE=10*1024*1024
SCRIPT_NAME="pipeDecoder.py"
COMMENT_STYLE = CodeUnit.PRE_COMMENT

try:
	command = askString(SCRIPT_NAME, "Shell command through which to pipe for decoding", "openssl enc -d -aes128 -nopad -K deadbeef -iv 0")
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

	p = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True, bufsize=PIPE_BUFFER_SIZE)
	stdout, stderr = p.communicate(bytes)
	bytes_decoded = stdout
	print "$ " + command
 	print stderr

	# only warn on "failed" execution, because, e.g., openssl will not return 0 if block length errors
	if p.returncode != 0:
		print "[!] WARNING: subprocess did not return with 0 (=success)"

	# only warn if there are less bytes returned than we send
	if len(bytes_decoded) < len(bytes):
		print "[!] WARNING: subprocess returned less bytes then we send for decoding"

	# however if we get more bytes than we send we fail because we have not enough space to write them
	if len(bytes_decoded) > len(bytes):
		print "[!] FAILED: subprocess returned a different amount of bytes then we provided"
	else:
		try:
			setBytes(begin, bytes_decoded)
			createBookmark(begin, SCRIPT_NAME, command)
			cu = currentProgram.getListing().getCodeUnitAt(begin)
			comment = SCRIPT_NAME + "\n"
			comment += command + "\n"
			comment += stderr + "\n"
			comment += "[send: " + hex(len(bytes)) + ", decoded: " + hex(len(bytes_decoded)) + "]"
			cu.setComment(COMMENT_STYLE, comment)
			print "[$] SUCCESS"
		except MemoryAccessException as e:
			print "[!] FAILED: " + str(e)
