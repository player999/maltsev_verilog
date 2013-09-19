#!/usr/bin/python3
import re
import pparser
import primitivelib
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
	node_list.extend([eval(str(node))])
	for i in range(0, len(node["arguments"])):
		if isinstance(node["arguments"][i]["value"], dict):
			arg = node["arguments"][i]["value"]
			node_list[-1]["arguments"][i]["id"] = node["arguments"][i]["value"]["id"]
			node_list[-1]["arguments"][i]["value"] = node["arguments"][i]["value"]["name"]
			node_list =  makeObjectInterconnectionList(arg, node_list)
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
	inputs_list = inputs_list[:-1]
	input_definition = input_definition + "\tinput wire RST;\n"
	input_definition = input_definition + "\tinput wire ST;\n"
	input_definition = input_definition + "\tinput wire CLK;\n"
	input_definition = input_definition + "\toutput wire RD;\n"
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

	print(input_definition)
	print("\n".join(res_def))
	print("\n".join(strd_list))
	print("\n".join(assigns))
	print("\n".join(modules_list))
	print(node["id"])

def generateRootOld(tree, acc, bw):
	template = open("root.tmp", "r").read()
	template = template.replace("%ROOT_NODE_ID%", tree["id"]);
	wires = []
	print(acc["wire"])
	for i in range(0,len(acc["wire"])):
		if acc["wire"][i] not in wires:
			wires.extend([acc["wire"][i]]) 
	acc["wire"] = wires
	input_definitions = ""
	inputs = ""
	wires = ""
	for i in range(0, len(acc["wire"])):
		if isWireType("in", acc["wire"][i]):
			input_definitions = input_definitions + "    input %s\n"%(acc["wire"][i])
			inputs = inputs + "%s, "%extractWireName(acc["wire"][i])
		else:
			wires = wires + "    %s\n"%(acc["wire"][i])
	inputs = inputs[:-2] 
	template = template.replace("%IN%", inputs);
	template = template.replace("%INPUT_DEFINITIONS%", input_definitions)
    
	modules = ""
	for modline in acc["module"]:
		modules = modules + "    %s\n"%(modline)
	template = template.replace("%MODULES%", modules)

	assignments = ""
	for ass in acc["start"]:
		assignments = assignments + "    %s\n"%(ass)
	assignments = assignments + "    assign RD = node%s_rd;\n"%(tree["id"])
	assignments = assignments + "    assign RES[%d:0] = node%s_res[%d:0];\n"%(int(bw)-1, tree["id"], int(bw)-1)
	template = template.replace("%ASSIGNMENTS%", assignments)
	template = template.replace("%WIRES%", wires)
	template = template.replace("%BUS_WIDTH%", str(bw))
	#Generate testbench
	template_tb = open("root_tb.tmp", "r").read()
	input_wires = ""
	input_regs = ""
	assign_wires = ""
	in_init = ""
	cnt = 0
	for arg in acc["wire"]:
		if isWireType("in", arg):
			wire = re.findall("^wire \[.*\] (.*);", arg)
			wire = wire[0]
			input_wires = input_wires + "\twire [%d-1:0] %s;\n"%(bw, wire)
			input_regs = input_regs + "\treg [%d-1:0] r%s;\n"%(bw, wire) 
			assign_wires = assign_wires + "\tassign %s = r%s;\n"%(wire, wire)
			if cnt == 0:
				in_init = in_init + "\tr%s = %d;\n"%(wire, 5)
			if cnt == 1:
				in_init = in_init + "\tr%s = %d;\n"%(wire, 2)
			cnt = cnt + 1
    
	template_tb = template_tb.replace("%INDEF%", input_wires + input_regs)
	template_tb = template_tb.replace("%ROOT_NODE_ID%", tree["id"])
	template_tb = template_tb.replace("%IN%", inputs)
	template_tb = template_tb.replace("%IN_ASSIGN%", assign_wires)
	template_tb = template_tb.replace("%SIM_TIME%", str(16000))
	template_tb = template_tb.replace("%IN_INIT%", in_init)    
	template_tb = template_tb.replace("%BUS_WIDTH%", str(bw))
	return template, template_tb
    
if __name__ == "__main__":
	line1 = "add(IN0,mul(IN1,IN2))"
	tree = pparser.parseExp(line1)
	tree = primitivelib.convertToPrimitives(tree)
	generateRoot(tree, 16)
