#!/usr/bin/python3
# -*- tab-width:4 -*-

from configs import *
import os

def generate(node, bw):
	#Fill template
	template = open(BASIS_FUNCTIONS_DIR + "/operation_o.tmp","r").read()
	template = template.replace("%NAME%", str(node["name"]) + str(node["id"]))
	template = template.replace("%BUS_WIDTH%", str(bw-1))
	if not os.path.exists(PROJECT_DIR):
		os.makedirs(PROJECT_DIR)
	f = open(PROJECT_DIR + "/node_%s%s"%(node["name"], node["id"] + ".v"),"w")
	f.write(template)
	f.close()
