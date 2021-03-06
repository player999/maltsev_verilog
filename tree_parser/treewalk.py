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
import preprocessor
import random

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
	#tree = lisparse.parse_program(term)
	tree = preprocessor.preprocess_text(term)
	tree = preprocessor.convert2primitives(tree)
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
	random.seed(7)
	if len(sys.argv) != 3:
		print("Incorrect arguments")
		print("filename [arg1,arg2,...]")
		quit()
	text = open(sys.argv[1], "r").read()
	tree = makeCode(text, 32)
	generateTestbench(tree, 32, eval(sys.argv[2]), 1000000)
