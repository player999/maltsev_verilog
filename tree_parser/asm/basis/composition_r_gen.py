#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import generateRoot
import treewalk
import os

def generate(node, bw):
	#Generate %PUSH_ARGUMENTS%
	push_arguments = ""
	for i in range(0, len(node["arguments"]))
		push_arguments = push_arguments + "\t\tmov rax, [rsp + %i]\n"%(16 + (len(node["arguments"]) - i) * 8)
		push_arguments = push_arguments + "\t\tpush rax\n"
	#Genetate G and H STACK_OFFSET	
	gstack_offset = len(node["arguments"]) * 8
	hstack_offset = (len(node["arguments"]) + 1) * 8

	#Generate H and G functions names
	g_function = "root_%s%s"%(node["static"][0]["name"], node["static"][0]["id"])
	h_function = "root_%s%s"%(node["static"][1]["name"], node["static"][1]["id"])

	#Generate H and G functions
	nodes_g = generateRoot.generateRoot(node["static"][0], bw)
	nodes_h = generateRoot.generateRoot(node["static"][1], bw)
	treewalk.generateNodes(nodes_g, bw)
	treewalk.generateNodes(nodes_h, bw)
	
	#Fill template
	template = open(BASIS_FUNCTIONS_DIR + "/composition_r.tmp","r").read()
	template = template.replace("%PUSH_ARGUMENTS%", push_arguments)
	template = template.replace("%GSTACK_OFFSET%", gstack_offset)
	template = template.replace("%HSTACK_OFFSET%", hstack_offset)
	template = template.replace("%G_FUNCTION%", g_function)
	template = template.replace("%H_FUNCTION%", h_function)
	template = template.replace("%NAME%", str(node["name"]) + str(node["id"]))
	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/node_%s%s"%(node["name"], node["id"] + ".s"),"w")
	f.write(template)
	f.close()
