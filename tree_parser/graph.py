#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import generateRoot

def nodeName(node):
	return node["name"] + node["id"]

def drawGraph(tree, fname):
	graph_text = "digraph Root {\n"
	graph_text = drawNode(tree, graph_text)
	graph_text = graph_text + "}\n"
	
	#Save to file
	f = open(PROJECT_DIR + "/%s"%fname,"w")
	f.write(graph_text)
	f.close()

def makeHTML(src_tree, primitive_tree):
	template = open(HTML_TEMPLATE, "r").read()
	template = template.replace("%JSON_SOURCE%", src_tree)
	template = template.replace("%JSON_PRIMITIVE%", primitive_tree)
	template = template.replace("%IMG_SOURCE%", SOURCE_IMG)
	template = template.replace("%IMG_PRIMITIVE%", PRIMITIVE_IMG)
	f = open(PROJECT_DIR + "/" + HTML_OUT, "w")
	f.write(template)
	f.close()

def makeMk():
	constants = open("configs.py","r").read()
	constants = constants.replace("\"","")
	constants = constants.replace(" ","")
	f = open(MK_INCLUDE, "w")
	f.write(constants)
	f.close()

def drawNode(node, graph_text):
	for i in range(0,len(node["arguments"])):
		if isinstance(node["arguments"][i]["value"], str):
			inid = node["name"] + node["id"] + "_" + node["arguments"][i]["value"]
			graph_text = graph_text + "%s->%s;\n"%(inid, nodeName(node))
			graph_text = graph_text + "%s [label=%s];\n"%(inid, node["arguments"][i]["value"])
		else:
			graph_text = graph_text + "%s->%s;\n"%(nodeName(node["arguments"][i]["value"]), nodeName(node))
			graph_text = drawNode(node["arguments"][i]["value"], graph_text)
	for i in range(0,len(node["static"])):
		if isinstance(node["static"][i], dict):
			graph_text = graph_text + "%s->%s[style=dotted];\n"%(nodeName(node["static"][i]), nodeName(node))
			graph_text = drawNode(node["static"][i], graph_text)
	return graph_text

if __name__ == "__main__":
	makeMk()
