#Colors all calls along the call graph to the current address
#@author 
#@category
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.program.model.address import Address
from ghidra.program.model.address import AddressSet
from java.awt import Color

def collect_calls(addresses, address):
	f = getFunctionContaining(address)
	if f == None :
		return
	print f.getName()
	e = f.getEntryPoint()
	for r in getReferencesTo(e):
		if r.getReferenceType().isCall() :
				a = r.getFromAddress()
				addresses.add(a)
				collect_calls(addresses, a)

addresses = AddressSet()

collect_calls(addresses, currentAddress)

setBackgroundColor(addresses, Color.RED)

