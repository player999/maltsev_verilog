#!/usr/bin/python3
import pparser

def tree2str(tree):
	if isinstance(tree,str):
		return tree
	if isinstance(tree,dict):
		arglist = ""
		for i in range(0,len(tree["arguments"])):
			arglist = arglist + tree2str(tree["arguments"][i])+","
		arglist = arglist[:-1]

		if tree["static"] != []:
			staticlist = ""
			for i in range(0,len(tree["static"])):
				staticlist = staticlist + tree2str(tree["static"][i])+","
			staticlist = staticlist[:-1]
			tree2 = "%s(%s;%s)"%(tree["name"], staticlist, arglist)
		else:
			tree2 = "%s(%s)"%(tree["name"], arglist)
		return tree2
	else:
		raise Exception("Unknown type of tree")
		

def checklib(node):
	if node["name"] == "add":
		return lib_add(node);
	elif node["name"] == "mul":
		return lib_mul(node);
	else:
		return node;


def lib_add(node):
	nc = node;
	node["name"] = "R"
	node["static"] = []
	node["static"].extend(["i(0;"+tree2str(nc["arguments"][0])+","+tree2str(nc["arguments"][1])+")"])
	node["static"].extend(["i(0;"+"s("+tree2str(nc["arguments"][0])+")"+","+tree2str(nc["arguments"][1])+",placeholder1)"])
	return node

def lib_mul(node):
	nc = node;
	#static2 = "i(0;sum(i(0;%X%,%Y%,placeholder1),i(2;%X%,%Y%,placeholder1)),%Y%,placeholder1)"
	#static2 = static2.replace("%X%",nc["arguments"][0])
	#static2 = static2.replace("%Y%",nc["arguments"][1])
	#print(static2)
	node["name"] = "R"
	node["static"] = []
	node["static"].extend(["o("+tree2str(nc["arguments"][0])+","+tree2str(nc["arguments"][1])+")"])
	#node["static"].extend([static2])
	node["static"].extend(["i(0;add("+tree2str(nc["arguments"][0])+","+tree2str(nc["arguments"][1])+"),"+tree2str(nc["arguments"][1])+"," + "placeholder1" + ")"])
	return node

