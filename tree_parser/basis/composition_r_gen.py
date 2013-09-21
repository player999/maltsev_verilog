#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import generateRoot
import treewalk
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

	#Generate %ADDITIONAL_IN%
	additional_in = "IN%d"%(len(node["arguments"]))

	#Generate H and G classes names
	g_class = "root_%s%s"%(node["static"][0]["name"], node["static"][0]["id"])
	h_class = "root_%s%s"%(node["static"][1]["name"], node["static"][1]["id"])

	#Generate %MAX_IN%
	max_in = "IN%d"%(len(node["arguments"])-1)

	#Generate H and G classes
	nodes_g = generateRoot.generateRoot(node["static"][0], bw)
	nodes_h = generateRoot.generateRoot(node["static"][1], bw)
	treewalk.generateNodes(nodes_g, bw)
	treewalk.generateNodes(nodes_h, bw)
	#Fill template
	template = open(BASIS_FUNCTIONS_DIR + "/composition_r.tmp","r").read()
	template = template.replace("%IN_LIST%", in_list)
	template = template.replace("%IN_DEF%", in_def)
	template = template.replace("%ADDITIONAL_IN%", additional_in)
	template = template.replace("%G_CLASS%", g_class)
	template = template.replace("%H_CLASS%", h_class)
	template = template.replace("%MAX_IN%", max_in)
	template = template.replace("%NAME%", str(node["name"]) + str(node["id"]))
	template = template.replace("%BUS_WIDTH%", str(bw-1))
	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/node_%s%s"%(node["name"], node["id"] + ".v"),"w")
	f.write(template)
	f.close()
