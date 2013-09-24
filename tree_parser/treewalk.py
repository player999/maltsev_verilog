#!/usr/bin/python3
# -*- tab-width:4 -*-
import pparser
import generateRoot
import subprocess
import primitivelib
import graph
import sys
import os
import json

from configs import *

def loadBasisList():
	basis_file = open(BASIS_FUNCTIONS_FILE, "r").readlines()
	basis_functions = []
	for entry in basis_file:
		entry = entry[:-1].split("\t")
		basis_functions.extend([{"mnemonics":entry[0], "file":entry[1]}])
	return basis_functions


def generateNode(node, basis_functions, bw):
	for entry in basis_functions:
		if entry["mnemonics"] == node["name"]:
			generator_name = entry["file"]+"_gen"
			generator = __import__(generator_name)
			generator.generate(node, bw)

def generateNodes(node_list, bw):
	basis_list = loadBasisList()
	for node in node_list:
		generateNode(node, basis_list, bw)

def makeVerilog(term, bw):
	sys.path.append(os.path.abspath(BASIS_FUNCTIONS_DIR))
	tree = pparser.parseExp(term)
	graph.drawGraph(tree, SOURCE_GRAPH)
	src_json  = json.dumps(tree, indent=4, separators=(',', ': '))
	f = open(PROJECT_DIR + "/" + SOURCE_JSON, "w")
	f.write(src_json)
	f.close()
	tree = primitivelib.convertToPrimitives(tree)
	node_list = generateRoot.generateRoot(tree, bw)
	generateNodes(node_list, bw)
	graph.drawGraph(tree, PRIMITIVE_GRAPH)
	primitive_json = json.dumps(tree, indent=4, separators=(',', ': '))
	f = open(PROJECT_DIR + "/" + PRIMITIVE_JSON, "w")
	f.write(primitive_json)
	graph.makeHTML(src_json, primitive_json)
	f.close()
	
	return tree

def generateTestbench(tree, bw, values, sim_time):
	in_count = len(generateRoot.makeInputWireList(tree, []))
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
	template = open("root_tb.tmp","r").read()
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
		

if __name__ == "__main__":
	line1 = "I(2,3;X,i(1;s(x),m(g(n),5)),Z)"
	line2 = "R(i(0;x,y),i(0;s(x),y);x,y)"
	line3 = "mul(x,y)"
	line4 = "R(i(0;x,y),i(0;s(x),y,z);x,y)"
	line5 = "add(IN0,IN1)"
	line6 = "add(IN0,mul(IN1,IN2))"
	line7 = "mul(IN0,IN1)"
	line8 = "add(add(mul(IN0,IN1),IN2),add(IN3,IN4))"
	tree = makeVerilog(line6, 16)
	generateTestbench(tree, 16, [3,4,5], 100000)

