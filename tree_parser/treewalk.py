#!/usr/bin/python3
# -*- tab-width:4 -*-
import pparser
import generateRoot
import subprocess
import primitivelib
import sys
import os

from configs import *

def drawGraph(graph, name):
	line = "digraph {\n";
	for entry in graph:
		line = line + "\t" + entry + ";\n"
	line = line + "}\n"
	arguments = ['dot', '-Tpng', '-o%s.png'%name]
	p = subprocess.Popen(arguments, stdin=subprocess.PIPE)
	p.stdin.write(line.encode('utf-8'))
	p.stdin.close()

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
	tree = primitivelib.convertToPrimitives(tree)
	node_list = generateRoot.generateRoot(tree, bw)
	generateNodes(node_list, bw)

if __name__ == "__main__":
	line1 = "I(2,3;X,i(1;s(x),m(g(n),5)),Z)"
	line2 = "R(i(0;x,y),i(0;s(x),y);x,y)"
	line3 = "mul(x,y)"
	line4 = "R(i(0;x,y),i(0;s(x),y,z);x,y)"
	line5 = "add(x,y)"
	line6 = "add(IN0,mul(IN1,IN2))"
	makeVerilog(line6, 16)
