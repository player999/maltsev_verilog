import generateRoot
import os
from configs import *
def generateTestbench(tree, bw, values, sim_time):
	in_count = len(list(set(generateRoot.makeInputWireList(tree, []))))

	#%NAME%
	name = tree["name"] + tree["id"]	

	#%IN_DEF%
	r_in_def = ""
	in_def = ""
	for i in range(0,in_count):
		r_in_def = r_in_def + "\treg [%d:0] rIN%d;\n"%(bw-1, i)
		in_def = in_def + "\twire [%d:0] IN%d;\n"%(bw-1, i)
	in_def = in_def + r_in_def[:-1]

	#%IN_LIST%o
	in_list = ""
	for i in range(0,in_count):
		in_list = in_list + "IN%d, "%i
	if in_list != "":
		in_list = ", " + in_list
		in_list = in_list[:-2]


	#%IN_ASSIGN%
	in_assign = ""
	for i in range(0, in_count):
		in_assign = in_assign + "\tassign IN%d = rIN%d;\n"%(i, i)
	in_assign = in_assign[:-1]
	
	#%IN_INIT%
	in_init = ""
	for i in range(0, in_count):
		in_init = in_init + "\trIN%d = %s;\n"%(i, str(values[i]))
	in_init = in_init[:-1]
	
	#%DUMP_FILE%
	dump_file = os.path.abspath(PROJECT_DIR + "/dump.vcd")
	
	#Fill template
	template = open(PLATFORM+"/root_tb.tmp","r").read()
	template = template.replace("%BUS_WIDTH%", str(bw-1))
	template = template.replace("%IN_DEF%", in_def)
	template = template.replace("%NAME%", name)
	template = template.replace("%IN_LIST%", in_list)
	template = template.replace("%IN_ASSIGN%", in_assign)
	template = template.replace("%DUMP_FILE%", dump_file)
	template = template.replace("%IN_INIT%", in_init)
	template = template.replace("%SIM_TIME%", str(sim_time))
	f = open(PROJECT_DIR + "/root_tb.v", "w")
	f.write(template)
	f.close()
