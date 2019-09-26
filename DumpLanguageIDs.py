#Dumps all available Language IDs to Console.
#@author 
#@category
#@keybinding 
#@menupath 
#@toolbar 

import ghidra.program.util.DefaultLanguageService

for langid in ghidra.program.util.DefaultLanguageService.getLanguageService().getLanguageDescriptions(True):
	print langid
