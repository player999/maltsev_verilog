#!/usr/bin/python3
#-*- tab-width:4 -*-

import re
import pparser
import primitivelib
import os
from configs import *

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
	#Eliminate clones
	new_list = []
	for i in range(0, len(rin_list)):
		if rin_list[i] in new_list:
			continue
		else:
			new_list.extend([rin_list[i]])
	rin_list = ", ".join(new_list)
	return rin_list


def makeObjectInterconnectionList(node, node_list):
	tmp_node = eval(str(node))
	for i in range(0, len(node["arguments"])):
		if isinstance(node["arguments"][i]["value"], dict):
			arg = node["arguments"][i]["value"]
			tmp_node["arguments"][i]["id"] = node["arguments"][i]["value"]["id"]
			tmp_node["arguments"][i]["value"] = node["arguments"][i]["value"]["name"]
			node_list =  makeObjectInterconnectionList(arg, node_list)
	node_list.extend([tmp_node])
	return node_list

def compareInputs(in_wire):
	res = re.findall("IN([0-9]*)", in_wire)
	if res != []:
		return int(res[0])
	else:
		raise Exception("compareInputs: Can not process wire")

def makeStartWireList(node, st_list):
	start = []
	for entry in node["arguments"]:
		if isinstance(entry["value"], dict):
			start.extend([entry["value"]["id"]])
			st_list = makeStartWireList(entry["value"], st_list)
	st_list.extend([{"id":node["id"], "assign":start}])
	return st_list


def getListById(Id, List):
	for entry in List:
		if entry["id"] == Id:
			return entry
	return 0


def generateRoot(node, bw):
	#IO list
	inputs_list = make_rinlist(node)
	if inputs_list == "":
		long_list = []
	else:
		long_list = inputs_list.split(", ")
	inputs_list = long_list
	input_definition = ""
	for entry in inputs_list:
		input_definition = input_definition + "\tinput wire [%d:0] %s;\n"%(bw-1, entry)
	input_definition = input_definition[:-1]
	node_list = makeObjectInterconnectionList(node, [])
	#Define st rd wires
	strd_list = [""]
	for entry in node_list:
		strd_list.extend(["\twire node_%s%s_rd;"%(entry["name"], entry["id"])])
		strd_list.extend(["\twire node_%s%s_st;"%(entry["name"], entry["id"])])
	
	#Define RES wires
	res_def = [""]
	for	entry in node_list:
		res_def.extend(["\twire [%d:0] node_%s%s_res;"%(bw - 1, entry["name"], entry["id"])])
	
	#Connect all start wires
	start_wires = makeStartWireList(node, [])	
	assigns = ["\tassign RES = node_%s%s_res;"%(node["name"], node["id"])]
	#Expression for RD wire
	rd_list = ""
	for entry in node_list:
		rd_list = rd_list + "node_%s%s_rd&"%(entry["name"],entry["id"])
	rd_list = rd_list[:-1]
	assigns.extend(["\tassign RDin = %s;"%(rd_list)])
	for entry in start_wires:
		if entry["assign"]:
			st_exp = ""
			for rd in entry["assign"]:
				st_exp = st_exp + "node_%s%s_rd&"%(getListById(rd, node_list)["name"], rd)
			st_exp = st_exp[:-1]
			assigns.extend(["\tassign node_%s%s_st = %s;"%(getListById(entry["id"], node_list)["name"], entry["id"], st_exp)])
		else:
			assigns.extend(["\tassign node_%s%s_st = ST;"%(getListById(entry["id"], node_list)["name"], entry["id"])])

	#Make modules list
	modules_list = [""]
	for entry in node_list:
		mod_in_list = ""
		for arg in entry["arguments"]:
			if "id" in arg.keys():
				mod_in_list = mod_in_list + "node_%s%s_res,"%(arg["value"], arg["id"])
			else:
				mod_in_list = mod_in_list + arg["value"]+","
		if mod_in_list != "":
			mod_in_list = mod_in_list[:-1]
		mod_name = "_%s%s"%(entry["name"],entry["id"])
		if mod_in_list == "":
			mod_string = "\tnode%s n%s(RST,%s,CLK,%s,%s);"%(mod_name, mod_name, "node%s_st"%mod_name, "node%s_rd"%mod_name, "node%s_res"%mod_name)
			modules_list.extend([mod_string])
		else:
			mod_string = "\tnode%s n%s(RST,%s,CLK,%s,%s,%s);"%(mod_name, mod_name, "node%s_st"%mod_name, "node%s_rd"%mod_name, "node%s_res"%mod_name, mod_in_list)
			modules_list.extend([mod_string])
	#Fill the template
	template = open(BASIS_FUNCTIONS_DIR + "/root.tmp", "r").read()
	template = template.replace("%INPUT_DEFINITIONS%",input_definition)
	wire_data = "\n".join(res_def) + "\n".join(strd_list)
	template = template.replace("%WIRES%", wire_data)
	template = template.replace("%ASSIGNMENTS%", "\n".join(assigns))
	template = template.replace("%MODULES%", "\n".join(modules_list))
	template = template.replace("%ROOT_NAME%", node["name"])
	template = template.replace("%ROOT_NODE_ID%", node["id"])
	template = template.replace("%BUS_WIDTH%", str(bw - 1))
	if len(inputs_list) == 0:
		template = template.replace("%IN%", "")
	else:
		template = template.replace("%IN%", ", " + ", ".join(inputs_list))
	#Save file 
	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/root_%s%s"%(node["name"], node["id"] + ".v"),"w")
	f.write(template)
	f.close()
	return node_list

   
if __name__ == "__main__":
	line1 = "add(IN0,mul(IN1,IN2))"
	tree = pparser.parseExp(line1)
	tree = primitivelib.convertToPrimitives(tree)
	generateRoot(tree, 16)
