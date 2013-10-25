#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import os

def generate(node, bw):
	#Load and fill template
	template = open(BASIS_FUNCTIONS_DIR + "/operation_i.tmp","r").read()
	template = template.replace("%OFFSET%", str(16 + 8 * (len(node["arguments"]) - int(node["static"][0]))))
	template = template.replace("%NAME%", str(node["name"]) + str(node["id"]))
	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/node_%s%s"%(node["name"], node["id"] + ".s"),"w")
	f.write(template)
	f.close()
