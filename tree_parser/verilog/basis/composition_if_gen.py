#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import generateRoot
import treewalk
import os

def generate(node, bw):
	#%IN%
	in_list = ""
	for i in range(0, len(node["arguments"])):
		in_list = in_list + "IN%d, "%i
	in_list = in_list[:-2] 

	#Generate %IN_DEF%
	in_def = ""
	for i in range(0, len(node["arguments"])):
		in_def = in_def + "   input wire [%d:0] IN%d;\n"%(bw - 1, i)
	nd_def = in_def[:-1]

	#Modules

	#Predicate
	pred_name = "root_%s%s"%(node["static"][2]["name"], node["static"][2]["id"])
	pred_node = generateRoot.generateRoot(node["static"][2], bw)
	treewalk.generateNodes(pred_node, bw)
	#Yes-block
	yes_name = "root_%s%s"%(node["static"][0]["name"], node["static"][0]["id"])
	yes_node = generateRoot.generateRoot(node["static"][0], bw)
	treewalk.generateNodes(yes_node, bw)

	#No-block
	no_name = "root_%s%s"%(node["static"][1]["name"], node["static"][1]["id"])
	no_node = generateRoot.generateRoot(node["static"][1], bw)
	treewalk.generateNodes(no_node, bw)

	
	#Fill template
	template = open(BASIS_FUNCTIONS_DIR + "/composition_if.tmp","r").read()
	template = template.replace("%IN%", in_list)
	template = template.replace("%IN_DEF%", in_def)
	template = template.replace("%MODULENAME%", str(node["name"]) + str(node["id"]))
	template = template.replace("%BW%", str(bw))
	template = template.replace("%PRED_MOD%", pred_name)
	template = template.replace("%YES_MOD%", yes_name)	
	template = template.replace("%NO_MOD%", no_name)

	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/node_%s%s"%(node["name"], node["id"] + ".v"),"w")
	f.write(template)
	f.close()
