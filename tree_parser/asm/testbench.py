import generateRoot
import os
from configs import *
def generateTestbench(tree, values):
	in_count = len(generateRoot.makeInVarList(tree, []))
	#%TESTING_BLOCK%
	testing_block = "root_" + tree["name"] + tree["id"]	
	
	#%RETURN_STACK%
	return_stack = "\tsub rsp, %d\n"%(in_count * 8)

	#%LOAD_ARGS%
	in_init = ""
	for i in range(0, in_count):
		in_init = in_init + "\tmov rax,%d;\n\tpush rax\n"%(values[i])
	
	#Fill template
	template = open(PLATFORM+"/root_tb.tmp","r").read()
	template = template.replace("%TESTING_BLOCK%", testing_block)
	template = template.replace("%LOAD_ARGS%", in_init)
	template = template.replace("%RETURN_STACK%", return_stack)
	f = open(PROJECT_DIR + "/root_tb.s", "w")
	f.write(template)
	f.close()
