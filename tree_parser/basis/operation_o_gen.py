#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import os

def generate(node, bw):
	#Generate %IN_LIST%
	in_list = ""
	for i in range(0, len(node["arguments"])):
		in_list = in_list + "IN%d, "%i
	in_list = in_list[:-2]

	#Generate %IN_DEF%
	in_def = ""
	for i in range(0, len(node["arguments"])):
		in_def = in_def + "input wire [%d:0] IN%d;\n"%(bw - 1, i)
	ind_def = in_def[:-1]

	#Fill template
	template = open(BASIS_FUNCTIONS_DIR + "/operation_o.tmp","r").read()
	template = template.replace("%IN_LIST%", in_list)
	template = template.replace("%IN_DEF%", in_def)
	template = template.replace("%NAME%", str(node["name"]) + str(node["id"]))
	template = template.replace("%BUS_WIDTH%", str(bw-1))
	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/node_%s%s"%(node["name"], node["id"] + ".v"),"w")
	f.write(template)
	f.close()
