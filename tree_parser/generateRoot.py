#!/usr/bin/python3
#-*- tab-width:4 -*-

import re
import pparser
import primitivelib
import os
from configs import *
		
def makeInputWireList(root_node, input_list):
	for arg in root_node["arguments"]:
		if isinstance(arg["value"], str):
			res = re.findall("PR([0-9]*)", arg["value"])
			if res == []:
				input_list.extend([arg["value"]])
		elif isinstance(arg["value"], dict):
			input_list = makeInputWireList(arg["value"], input_list)
		else:
			raise Exception("makeInputWireList: Unknown type of argument")
	input_list = list(set(input_list))
	input_list = sorted(input_list, key=compareInputs)		
	return input_list

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
	inputs_list = makeInputWireList(node, [])
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
	assigns = ["\tassign RD = node_%s%s_rd;"%(node["name"], node["id"])]
	assigns.extend(["\tassign RES = node_%s%s_res;"%(node["name"], node["id"])])
	for entry in start_wires:
		if entry["assign"]:
			st_exp = ""
			for rd in entry["assign"]:
				st_exp = st_exp + "node_%s%s_rd&"%(getListById(entry["id"], node_list)["name"], rd)
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
				mod_in_list = mod_in_list + "node_%s%s_res,"%(arg["id"], arg["value"])
			else:
				mod_in_list = mod_in_list + arg["value"]+","
		mod_in_list = mod_in_list[:-1]
		mod_name = "_%s%s"%(entry["name"],entry["id"])
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
	template = template.replace("%IN%", ", ".join(inputs_list))
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
