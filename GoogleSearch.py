#Search a function name via Google
#@author 
#@category
#@keybinding ALT-SHIFT-G
#@menupath 
#@toolbar 

DEFAULT_BROWSER='firefox'

GOOGLE_SEARCH_PREFIX = "https://www.google.com/search?btnI&q="
DUCKDUCKGO_SEARCH_PREFIX = "https://duckduckgo.com/?q=!ducky "
SEARCH_PREFIX = GOOGLE_SEARCH_PREFIX

from subprocess import Popen
from ghidra.program.model.symbol import FlowType

def search_address(address):
	search = None
	f = getFunctionAt(address)
	if f:
		search = f.getName()
		if search.startswith("FID_conflict:"):
			search = search[13:]
	return search

search = None

for r in getReferencesFrom(currentAddress):
	if r.isExternalReference():
		search = r.getLibraryName() + " " + r.getLabel()
		break
	t = r.getReferenceType()
	if t == FlowType.UNCONDITIONAL_CALL:
		search = search_address(r.getToAddress())
		if search:
			break

if search == None:
	search = search_address(currentAddress)

if search:
	search = SEARCH_PREFIX + search
	print "Opening: " + search
	Popen([DEFAULT_BROWSER, search])
else:
	print "FAILED: Nothing found to search."

