#Search and reasemble ASCII stack strings formed via repeated instructions of:
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
# Issues:
# - Only works when instructions loading the string are in loading order (that is destination order is not evaluated)
# - Only works with ASCII
#@author 
#@category Search
#@keybinding 
#@menupath Search.Simple Stack Strings
#@toolbar 

from ghidra.program.model.listing import CodeUnit

SCRIPT_NAME="SearchSimpleStackStrings.py"
COMMENT_STYLE = CodeUnit.PRE_COMMENT
MIN_STRING_LEN = 4

# TODO: actually call our SimpleStackStrings.py script here instead of copy pasting its code :(
def try_reassemble_stackstring(address):
	stack_str = ""
	inst = getInstructionAt(address)

	skip = 0
	ascii = 0
	nonzero = 0
	total = 0
	while inst and (inst.getScalar(1) or inst.getScalar(0)):
		if inst.getScalar(1) == None:
			value = inst.getScalar(0).value
		else:
			value = inst.getScalar(1).value
		stack_str_part = ""
		# FIXME: here is a bug: null bytes are dropped :/
		while value > 0:
			c = value&0xff
			if c >= ord(' ') and c <= ord('~'):
				ascii += 1
			else:
				c = ord('.') # strip non-ascii chars
			if c != 0:
				nonzero += 1
			total += 1
			stack_str_part += chr(c)
			value = value>>8

		stack_str += stack_str_part
		#print hex(value) + ": \"" + stack_str_part + "\" of \"" + stack_str + "\""

		inst = inst.getNext()
		skip += 1

	if nonzero < MIN_STRING_LEN or total == 0 or ascii / float(total) < 0.49:
		# likely not a string
		return skip

	print str(address) + ": " + stack_str
	createBookmark(address, SCRIPT_NAME, stack_str)

	codeUnit = listing.getCodeUnitAt(address)
	comment = codeUnit.getComment(COMMENT_STYLE)
	if comment == None or comment == "":
		comment = ""
	else:
		comment += "\n"
	comment += SCRIPT_NAME + ": " + stack_str
	codeUnit.setComment(codeUnit.PRE_COMMENT, comment)

	return skip


listing = currentProgram.getListing()
symbolTable = currentProgram.getSymbolTable()

for symbol in symbolTable.getAllSymbols(False):
	func = getFunctionAt(symbol.getAddress())
	if func == None or func.getProgram() == None:
		continue
	iter = func.getProgram().getListing().getCodeUnits(func.getBody(), True)
	skip = 0
	for i in iter:
		if skip<=0 and (i.getScalar(1) or i.getScalar(0)):
			skip = try_reassemble_stackstring(i.getAddress())
		skip -= 1

