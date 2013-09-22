#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import generateRoot

def nodeName(node):
	return node["name"] + node["id"]

def drawGraph(tree):
	graph_text = "digraph Root {\n"
	graph_text = drawNode(tree, graph_text)
	#input_list = generateRoot.makeInputWireList(tree, [])
	#input_list = " ".join(input_list)
	#graph_text = graph_text + "{rank=same; %s}\n"%input_list
	graph_text = graph_text + "}\n"
	

	#Save to file
	f = open(PROJECT_DIR + "/graph.txt","w")
	f.write(graph_text)
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
		#if isinstance(node["static"][i], str):
		#	graph_text = graph_text + "%s->%s[style=dotted];\n"%(nodeName(node), str(node["static"][i]))
	return graph_text
