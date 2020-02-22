#Reasemble an ASCII stack string formed via repeated instructions of:
# MOV dword ptr [0xffffff6c + EBP],0x70747468
# MOV dword ptr [0xffffff70 + EBP],0x2f2f3a73
# MOV dword ptr [0xffffff78 + EBP],0x66746f68
# ...
#
# OR
# 
# MOV byte ptr [EBP + 0x10],0x68
# MOV byte ptr [EBP + 0x11],0x74
# MOV byte ptr [EBP + 0x12],0x68
# ...
#
# Set current address to beginning of first instruction of above stack string code segment.
# The script will write the assembled string as a comment.
#
# Issues:
# - Only works when instructions loading the string are in loading order (that is destination order is not evaluated)
# - Only works with ASCII
#@author 
#@category
#@keybinding 
#@menupath Tools.Decoders.Simple Stack Strings
#@toolbar 

from ghidra.program.model.listing import CodeUnit

SCRIPT_NAME="SimpleStackStrings.py"
COMMENT_STYLE = CodeUnit.PRE_COMMENT

listing = currentProgram.getListing()

stack_str = ""
inst = getInstructionAt(currentAddress)

while inst and (inst.getScalar(1) or inst.getScalar(0)):
	if inst.getScalar(1) == None:
		value = inst.getScalar(0).value
	else:
		value = inst.getScalar(1).value
	stack_str_part = ""
	# FIXME: here is a bug: null bytes are dropped :/
	while value > 0:
		stack_str_part += chr(value&0xff)
		value = value>>8

	stack_str += stack_str_part
	print hex(value) + ": \"" + stack_str_part + "\" of \"" + stack_str + "\""

	inst = inst.getNext()

comment = SCRIPT_NAME + ": " + stack_str
codeUnit = listing.getCodeUnitAt(currentAddress)
codeUnit.setComment(codeUnit.PRE_COMMENT, comment)

print "Full string: " + stack_str

