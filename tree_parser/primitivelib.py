#!/usr/bin/python3
import pparser

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
	node["static"].extend(["i(0;"+nc["arguments"][0]+","+nc["arguments"][1]+")"])
	node["static"].extend(["i(0;"+"s("+nc["arguments"][0]+")"+","+nc["arguments"][1]+",placeholder1)"])
	return node

def lib_mul(node):
	nc = node;
	#static2 = "i(0;sum(i(0;%X%,%Y%,placeholder1),i(2;%X%,%Y%,placeholder1)),%Y%,placeholder1)"
	#static2 = static2.replace("%X%",nc["arguments"][0])
	#static2 = static2.replace("%Y%",nc["arguments"][1])
	#print(static2)
	node["name"] = "R"
	node["static"] = []
	node["static"].extend(["o("+nc["arguments"][0]+","+nc["arguments"][1]+")"])
	#node["static"].extend([static2])
	node["static"].extend(["i(0;add("+nc["arguments"][0]+","+nc["arguments"][1]+"),"+nc["arguments"][1]+"," + "placeholder1" + ")"])
	return node

