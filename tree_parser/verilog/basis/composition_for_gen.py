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
			input_list.extend(["r" + root_node["arguments"][i]["value"]])
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
				rin_list.extend(["r" + node["arguments"][i]["value"]])
	#Eliminate clones
	new_list = []
	for i in range(0, len(rin_list)):
		if rin_list[i] in new_list:
			continue
		else:
			new_list.extend([rin_list[i]])
	rin_list = ", ".join(new_list)
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
	
	#Generate %rIN_DEF%
	rin_def = ""
	for i in range(0, len(node["arguments"])):
		rin_def = rin_def + "   reg [%d:0] rIN%d;\n"%(bw - 1, i)
	rin_def = rin_def[:-1]

	#Generate %SOUT_DEF%
	sout_def = ""
	for i in range(0, len(node["arguments"])):
		sout_def = sout_def + "   wire [%d:0] SOUT%d;\n"%(bw - 1, i)
	sout_def = sout_def[:-1]

	#Generate %rSOUT_DEF%
	rsout_def = ""
	for i in range(0, len(node["arguments"])):
		rsout_def = rsout_def + "   reg [%d:0] rSOUT%d;\n"%(bw - 1, i)
	rsout_def = rsout_def[:-1]

	#Generate %RD_DEF%
	rd_def = ""
	for i in range(0, len(node["arguments"])):
		rd_def = rd_def + "   wire RD%d;\n"%(i)
	rd_def = rd_def[:-1]

	#Generate %ST_DEF%
	st_def = ""
	for i in range(0, len(node["arguments"])):
		st_def = st_def + "   reg ST%d;\n"%(i)
	st_def = st_def[:-1]

	#Generate %RD_AND%
	rd_and = ""
	for i in range(0, len(node["arguments"])):
		rd_and = rd_and + "RD%d & "%i
	rd_and = rd_and[:-3]

	#Generate %rSOUT_ZERO%
	rsout_zero = ""
	for i in range(0, len(node["arguments"])):
		rsout_zero = rsout_zero + "        rSOUT%d = 0;\n"%i
	rsout_zero = rsout_zero[:-1]

	#Generate %ST_ZERO%
	st_zero = ""
	for i in range(0, len(node["arguments"])):
		st_zero = st_zero + "        ST%d = 0;\n"%i
	st_zero = st_zero[:-1]

	#Generate %ST_ONE%
	st_one = ""
	for i in range(0, len(node["arguments"])):
		st_one = st_one + "        ST%d = 1;\n"%i
	st_one = st_one[:-1]

	#Generate %rIN_ZERO%
	rin_zero = ""
	for i in range(0, len(node["arguments"])):
		rin_zero = rin_zero + "        rIN%d = 0;\n"%i
	rin_zero = rin_zero[:-1]



	#Generate %rIN_rSOUT%
	rin_rsout = ""
	for i in range(0, len(node["arguments"])):
		rin_rsout = rin_rsout + "        rIN%d = rSOUT%d;\n"%(i,i)
	rin_rsout = rin_rsout[:-1]


	#Generate %rIN_SOUT%
	rin_sout = ""
	for i in range(0, len(node["arguments"])):
		rin_sout = rin_sout + "        rIN%d = SOUT%d;\n"%(i,i)
	rin_sout = rin_sout[:-1]

	#Generate %rSOUT_SOUT%
	rsout_sout = ""
	for i in range(0, len(node["arguments"])):
		rsout_sout = rsout_sout + "        rSOUT%d = SOUT%d;\n"%(i,i)
	rsout_sout = rsout_sout[:-1]


	#Generate %rIN_IN%
	rin_in = ""
	for i in range(0, len(node["arguments"])):
		rin_in = rin_in + "        rIN%d = IN%d;\n"%(i,i)
	rin_in = rin_in[:-1]

	#Module example
	#   modulename1 mod1(RST, ST1, CLK, RD1, SOUT1, rIN0, rIN1, rIN2...);
	
	#Generate %IN_MODULES%
	print("==================================")
	print(node)
	in_modules = ""
	for i in range(0, len(node["arguments"])):
		print("================")
		print(node["arguments"])
		print("================")
		print(node["static"][i]["arguments"])
		print("================")
		print(in_list)
		print("================")
		class_name = "root_%s%s"%(node["static"][i]["name"], node["static"][i]["id"])
		rin_list = make_rinlist(node["static"][i])
		if rin_list == "":
			in_modules = in_modules + "   %s mod%d(RST, ST%d, CLK, RD%d, SOUT%d);\n"%(class_name, i, i, i, i)
		else:
			in_modules = in_modules + "   %s mod%d(RST, ST%d, CLK, RD%d, SOUT%d, %s);\n"%(class_name, i, i, i, i, rin_list)
		mode_node = generateRoot.generateRoot(node["static"][i], bw)
		treewalk.generateNodes(mode_node, bw)
	in_modules = in_modules[:-1] 
	
	#Generate %PRED_MODULE%
	class_name = "root_%s%s"%(node["static"][-1]["name"], node["static"][-1]["id"])
	mode_node = generateRoot.generateRoot(node["static"][-1], bw)
	treewalk.generateNodes(mode_node, bw)
	print("================")
	print(node["arguments"])
	print("================")
	print(node["static"][-1]["arguments"])
	print("================")
	print(in_list)
	print("================")
	rin_list = make_rinlist(node["static"][-1])
	if rin_list == "":
		pred_module = "   %s pred(RST, pST, CLK, pRD, pRES);\n"%(class_name)
	else:
		pred_module = "   %s pred(RST, pST, CLK, pRD, pRES, %s);\n"%(class_name, rin_list)
	#Fill template
	template = open(BASIS_FUNCTIONS_DIR + "/composition_for.tmp","r").read()
	template = template.replace("%IN%", in_list)
	template = template.replace("%IN_DEF%", in_def)
	template = template.replace("%MODULENAME%", str(node["name"]) + str(node["id"]))
	template = template.replace("%rIN_DEF%", rin_def)
	template = template.replace("%SOUT_DEF%", sout_def)
	template = template.replace("%rSOUT_DEF%", rsout_def)
	template = template.replace("%RD_DEF%", rd_def)
	template = template.replace("%ST_DEF%", st_def)
	template = template.replace("%RD_AND%", rd_and)
	template = template.replace("%rSOUT_ZERO%", rsout_zero)
	template = template.replace("%ST_ZERO%", st_zero)
	template = template.replace("%rIN_ZERO%", rin_zero)
	template = template.replace("%ST_ONE%", st_one)
	template = template.replace("%rSOUT_SOUT%", rsout_sout)
	template = template.replace("%rIN_IN%", rin_in)
	template = template.replace("%rIN_rSOUT%", rin_rsout)
	template = template.replace("%rIN_SOUT%", rin_sout)
	template = template.replace("%BW%", str(bw))
	template = template.replace("%IN_MODULES%", in_modules)
	template = template.replace("%PRED_MODULE%", pred_module)

	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/node_%s%s"%(node["name"], node["id"] + ".v"),"w")
	f.write(template)
	f.close()
