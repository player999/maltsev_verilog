#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import generateRoot
import treewalk
import os
import re

def makeInputWireList(root_node, input_list):
	for i in range(0, len(root_node["arguments"])):
		if isinstance(root_node["arguments"][i]["value"], str):
			input_list.extend([root_node["arguments"][i]["value"]])
		elif isinstance(root_node["arguments"][i]["value"], dict):
			input_list = makeInputWireList(root_node["arguments"][i]["value"], input_list)
		else:
			raise Exception("makeInputWireList: Unknown type of argument")
	return input_list


def make_rinlist(node):
	if len(node["static"]) == 0:
		rin_list = makeInputWireList(node, [])
	else:
		rin_list = []
		for i in range(0,len(node["arguments"])):
			if isinstance(node["arguments"][i]["value"], str):
				rin_list.extend([node["arguments"][i]["value"]])
			if isinstance(node["arguments"][i]["value"], dict):
				rin_list = makeInputWireList(node["arguments"][i]["value"], rin_list)
	#Eliminate clones
	new_list = []
	for i in range(0, len(rin_list)):
		if rin_list[i] in new_list:
			continue
		else:
			new_list.extend([rin_list[i]])
	if rin_list != []:
		rin_list =", " + ", ".join(new_list)
	else:
		rin_list = ""
	return rin_list


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

	#YIN
	yin = make_rinlist(node["static"][0])

	#NIN
	nin = make_rinlist(node["static"][1])

	#PIN
	pin = make_rinlist(node["static"][2])

	#Fill template
	template = open(BASIS_FUNCTIONS_DIR + "/composition_if.tmp","r").read()
	template = template.replace("%IN%", in_list)
	template = template.replace("%YIN%", yin)
	template = template.replace("%NIN%", nin)
	template = template.replace("%PIN%", pin)
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
