#!/usr/bin/python3
import pparser
import random 
import re
from configs import *

def tree2str(tree):
	if isinstance(tree["path"],str):
		return tree["path"]
	if isinstance(tree["path"],dict):
		arglist = ""
		for i in range(0,len(tree["path"]["arguments"])):
			arglist = arglist + tree2str(tree["path"]["arguments"][i])+","
		arglist = arglist[:-1]
		if tree["path"]["static"] != []:
			staticlist = ""
			for i in range(0,len(tree["path"]["static"])):
				staticlist = staticlist + tree2str(tree["path"]["static"][i])+","
			staticlist = staticlist[:-1]
			tree2 = "%s(%s;%s)"%(tree["path"]["name"], staticlist, arglist)
		else:
			tree2 = "%s(%s)"%(tree["path"]["name"], arglist)
		return tree2
	else:
		raise Exception("Unknown type of tree")

def loadBasis():
	basis = open(BASIS_FUNCTIONS_FILE, "r").readlines()
	for i in range(0, len(basis)):
		basis[i] = basis[i].split('\t')
		basis[i][1] = basis[i][-1][:-1]
		basis[i] = tuple(basis[i])
	return basis

def loadLibrary():
	lib = open(LIBRARY_FUNCTIONS_FILE, "r").readlines()
	for i in range(0, len(lib)):
		lib[i] = lib[i].split('\t')
		lib[i][1] = lib[i][-1][:-1]
		lib[i] = tuple(lib[i])
	functions = []
	for fun in lib:
		description_file = open(LIBRARY_FUNCTIONS_DIR + "/" + fun[1] + ".fun","r").readlines()
		info_line = description_file[0][:-1].split('\t')
		function = {}
		function["mnemonic"] = info_line[0]
		function["inputs"] = int(info_line[1])
		function["static"] = int(info_line[2])
		function["generator"] = info_line[3]
		if function["generator"] == "None":
			function["template"] = "".join(description_file[1:])
		functions.extend([function])
	return functions

def convertToPrimitives(node):
	basis = loadBasis()
	library = loadLibrary()
	node = nodeWalker(node, basis, library)
	return node

def nodeWalker(node, basis, library):
	node = checkLib(node, basis, library)
	for i in range(0, len(node["arguments"])):
		if isinstance(node["arguments"][i]["value"], dict):
			node["arguments"][i]["value"] = nodeWalker(node["arguments"][i]["value"], basis, library)
	for i in range(0, len(node["static"])):
		if isinstance(node["static"][i], dict):
			node["static"][i] = nodeWalker(node["static"][i], basis, library)
	return node

def checkLib(node, basis, library):
	good_flag = 0
	for bf in basis:
		if bf[0] == node["name"]:
			return node
	for fun in library:
		if fun["mnemonic"] == node["name"]:
			node = applyLibraryFunction(node, fun)
			node = nodeWalker(node, basis, library)
			good_flag = 1
	if good_flag == 0:
		raise Exception("checkLib: Unknown function!")
	return node
	
def applyLibraryFunction(node, fun):
	if len(node["arguments"]) != fun["inputs"]:
		raise Exception("applyLibraryFunction: Input size missmatch")
	if len(node["static"]) != fun["static"]:
		raise Exception("applyLibraryFunction: Static size missmatch")
	if fun["generator"] == "None":
		template = fun["template"]
		id_res = re.findall("%ID([0-9]*)%", template)
		for idx in id_res:
			template = template.replace("%%ID%s%%"%(idx), str(int(99999 + random.random() * 900000)))
		arg_res = re.findall("%IN([0-9]*)%", template)
		for arg in arg_res:
			arg = int(arg)
			for argf in node["arguments"]:
				if argf["no"] == arg:
					if isinstance(argf["value"], str):
						template = template.replace("%%IN%d%%"%(arg), "\"%s\""%(argf["value"]))
					elif isinstance(argf["value"], dict):
						template = template.replace("%%IN%d%%"%(arg), str(argf["value"]))
					else:
						raise Exception("applyLibraryFunction: Inappropriate type of argument.")
	else:
		raise Exception("TODO: Finish custom generator")
	template = template.replace("\n","")
	template = template.replace(" ","")
	template = template.replace("\t","")
	template = template.replace("\'","\"")
	return eval(template)

if __name__ == "__main__":
	line1 = "add(x,mul(y,z))"
	node = pparser.parseExp(line1)
	node = convertToPrimitives(node)
	print(node)
