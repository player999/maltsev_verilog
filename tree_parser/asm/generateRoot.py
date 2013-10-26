#!/usr/bin/python3
#-*- tab-width:4 -*-

import re
import pparser
import primitivelib
import os
from configs import *
		
def makeInVarList(root_node, input_list):
	for arg in root_node["arguments"]:
		if isinstance(arg["value"], str):
			res = re.findall("PR([0-9]*)", arg["value"])
			if res == []:
				input_list.extend([arg["value"]])
		elif isinstance(arg["value"], dict):
			input_list = makeInVarList(arg["value"], input_list)
		else:
			raise Exception("makeInVar: Unknown type of argument")
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

def generateCallText(module_entry):
	#call_text = "\tpush rbp\n\tmov rbp, rsp\n"
	call_text=""
	#pushing data
	for i in range(0, len(module_entry["arguments"])):
		#load to register
		if "id" in module_entry["arguments"][i]: 
			call_text = call_text + "\tmov rax, [node_%s%s_res]\n"%(module_entry["arguments"][i]["value"], module_entry["arguments"][i]["id"])
		else:
			call_text = call_text + "\tmov rax, [%s]\n"%(module_entry["arguments"][i]["value"])
		#push
		call_text = call_text + "\tpush rax\n"
	#call
	call_text = call_text + "\tcall node_%s%s\n"%(module_entry["name"], module_entry["id"])
	call_text = call_text + "\tmov [node_%s%s_res], rax\n"%(module_entry["name"], module_entry["id"])
	call_text = call_text + "\tsub rsp, %d\n" % (len(module_entry["arguments"]) * 8)
	#call_text = call_text + "\tpop rbp\n\n"
	return call_text

def generateRoot(node, bw):
	#var_list
	inputs_list = makeInVarList(node, [])
	var_list = ""
	for entry in inputs_list:
		var_list = var_list + "\t%s: dq 0\n"%(entry)
	#import list
	import_list = ""
	node_list = makeObjectInterconnectionList(node, [])
	for i in range(0, len(node_list)):
		import_list = import_list + "\textern node_%s%s\n"%(node_list[i]["name"], node_list[i]["id"])

	#add res wires
	res_def = [""]
	for	entry in node_list:
		var_list = var_list + "\tnode_%s%s_res: dq 0\n"%(entry["name"], entry["id"])
	
	#load_inputs
	load_inputs = ""
	for i in range(0, len(inputs_list)):
		load_inputs = load_inputs + "\tmov rax, [rsp + %d]\n" %(8 + 8 * (len(inputs_list) - i))
		load_inputs = load_inputs + "\tmov [%s], rax\n"%(inputs_list[i])
	#Make modules list
	call_text = ""
	for entry in node_list:
		call_text = call_text + generateCallText(entry)
	#Answer
	answer = "\tmov rax, [node_%s%s_res]\n"%(node["name"], node["id"])
	#Fill the template
	template = open(BASIS_FUNCTIONS_DIR + "/root.tmp", "r").read()
	template = template.replace("%VARIABLES%", var_list)
	template = template.replace("%IMPORT%", import_list)
	template = template.replace("%LOAD_INPUTS%", load_inputs)
	template = template.replace("%ROOT_NAME%", node["name"])
	template = template.replace("%ROOT_NODE_ID%", node["id"])
	template = template.replace("%CALLS%", call_text)
	template = template.replace("%ANSWER%", answer)
	#Save file
	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/root_%s%s"%(node["name"], node["id"] + ".s"),"w")
	f.write(template)
	f.close()
	return node_list

   
if __name__ == "__main__":
	line1 = "add(IN0,mul(IN1,IN2))"
	tree = pparser.parseExp(line1)
	tree = primitivelib.convertToPrimitives(tree)
	generateRoot(tree, 16)
