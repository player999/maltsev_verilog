#!/usr/bin/python3
# -*- tab-width:4 -*-
import pparser
import subprocess
import primitivelib
import graph
import sys
import os
import json
import lisparse

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

def makeCode(term, bw):
	sys.path.append(os.path.abspath(BASIS_FUNCTIONS_DIR))
	sys.path.append(os.path.abspath(PLATFORM))
	#tree = pparser.parseExp(term)
	#print(tree)
	tree = lisparse.parse_program(term)
	print(tree)
	graph.drawGraph(tree, SOURCE_GRAPH)
	src_json  = json.dumps(tree, indent=4, separators=(',', ': '))
	f = open(PROJECT_DIR + "/" + SOURCE_JSON, "w")
	f.write(src_json)
	f.close()
	tree = primitivelib.convertToPrimitives(tree)
	rootgen = __import__("generateRoot")
	node_list = rootgen.generateRoot(tree, bw)
	generateNodes(node_list, bw)
	graph.drawGraph(tree, PRIMITIVE_GRAPH)
	primitive_json = json.dumps(tree, indent=4, separators=(',', ': '))
	f = open(PROJECT_DIR + "/" + PRIMITIVE_JSON, "w")
	f.write(primitive_json)
	graph.makeHTML(src_json, primitive_json)
	f.close()	
	return tree

def generateTestbench(tree, bw, values, sim_time):
	tbgen = __import__("testbench")
	if PLATFORM == "verilog":  
		tbgen.generateTestbench(tree, bw, values, sim_time)
	elif PLATFORM == "asm":
		tbgen.generateTestbench(tree, values)

if __name__ == "__main__":
	line1 = "I(2,3;X,i(1;s(x),m(g(n),5)),Z)"
	line2 = "R(i(0;x,y),i(0;s(x),y);x,y)"
	line3 = "mul(IN0,IN1)"
	line4 = "R(i(0;x,y),i(0;s(x),y,z);x,y)"
	line5 = "add(IN0,IN1)"
	line6 = "add(IN0,mul(IN1,IN2))"
	line7 = "mul(IN0,IN1)"
	line8 = "add(add(mul(IN0,IN1),IN2),add(IN3,IN4))"
	line9 = "(mul (IN2 IN1))"
	line10 = "(IF ((o (2) (IN1 IN2)) (o (2) (IN1 IN2)) (o (2) (IN1 IN2))) (IN1,IN2))"
	tree = makeCode(line10, 16)
	generateTestbench(tree, 16, [3,4], 100000)

