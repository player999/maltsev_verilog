#!/usr/bin/python3
import pparser
import generateRoot
import subprocess
import operation_o_gen
import operation_i_gen
import operation_s_gen
import composition_r_gen
import primitivelib

def drawGraph(graph, name):
	line = "digraph {\n";
	for entry in graph:
		line = line + "\t" + entry + ";\n"
	line = line + "}\n"
	arguments = ['dot', '-Tpng', '-o%s.png'%name]
	p = subprocess.Popen(arguments, stdin=subprocess.PIPE)
	p.stdin.write(line.encode('utf-8'))
	p.stdin.close()

def collect_inputs(root):
	inputs = []
	for i in range(0, len(root["arguments"])):
		if isinstance(root["arguments"][i], str):
			inputs.extend([root["arguments"][i]])
		else:
			inputs.extend(collect_inputs(root["arguments"][i]))
	in_list = []
	for i in range(0,len(inputs)):
		if inputs[i] not in in_list:
			in_list.extend([inputs[i]])
	return in_list

def arrange_inputs(inputs, arguments):
	arranged_list = []
	for i in range(0,len(inputs)):
		if (inputs[i] not in arranged_list) and (inputs [i] not in arguments):
			arranged_list.extend([inputs[i]])
	for i in range(0,len(arguments)):
		if isinstance(arguments[i],str):
			arranged_list.extend([arguments[i]])

def treeWalk(tree, parentNode, accumulator, graph, bw):
	if isinstance(tree, dict):
		tree = primitivelib.checklib(tree)
		accumulator = generateAccEntry(tree, accumulator, bw)
		generateNode(tree, bw)
	
	if parentNode == None:
		graph.extend(["%s->%s"%(tree["id"], "root")])
	else:
		graph.extend(["%s->%s"%(tree["id"], parentNode["id"])])
	for leaf in tree["arguments"]:	
		if isinstance(leaf, dict):
			accumulator, graph = treeWalk(leaf, tree, accumulator, graph, bw)
		else:
			graph.extend(["%s->%s"%(leaf, tree["id"])])
	return accumulator, graph

def generateNode(node, bw):
	if node["name"] == "o":
		operation_o_gen.generate_o(bw, len(node["arguments"]), node["id"])
	elif node["name"] == "i":
		operation_i_gen.generate_i(bw, len(node["arguments"]), node["static"][0], node["id"])
	elif node["name"] == "s":
		operation_s_gen.generate_s(bw, node["id"])
	elif node["name"] == "R":
		g = node["static"][0]
		h = node["static"][1]
		tree_g = pparser.parseParentheses(g)
		tree_h = pparser.parseParentheses(h)
		accumulatorg = {}
		accumulatorg["start"] = []
		accumulatorg["module"] = []
		accumulatorg["wire"] = ["wire [%d-1:0] node%s_res;"%(16, tree_g["id"])]
		graph = []
		gacc,graph = treeWalk(tree_g, None, accumulatorg, graph, 16)
		(flg, tbg) = generateRoot.generateRoot(tree_g, gacc, 16)
		drawGraph(graph,"root%s"%tree_g["id"])
		f = open("root%s.v"%(tree_g["id"]), "w")
		f.write(flg)
		f.close()
		f = open("root%s_tb.v"%(tree_g["id"]), "w")
		f.write(tbg)
		f.close()
		accumulatorh = {}
		accumulatorh["start"] = []
		accumulatorh["module"] = []
		accumulatorh["wire"] = ["wire [%d-1:0] node%s_res;"%(16, tree_h["id"])]
		graph = []
		hacc, graph = treeWalk(tree_h, None, accumulatorh, graph, 16)
		(flh, tbh) = generateRoot.generateRoot(tree_h, hacc, 16)
		drawGraph(graph,"root%s"%tree_h["id"])
		f = open("root%s.v"%(tree_h["id"]), "w")
		f.write(flh)
		f.close()
		f = open("root%s_tb.v"%(tree_h["id"]), "w")
		f.write(tbh)
		f.close()
		total_inputs = collect_inputs(tree_h)
		arrange_inputs(total_inputs, node["arguments"])
		composition_r_gen.generate_r(bw, total_inputs, tree_g["id"], tree_h["id"], node["id"])
	else:
		operation_o_gen.generate_o(bw, len(node["arguments"]), node["id"])

def generateAccEntry(node, accumulator, bw):
	if isinstance(node, str):
		return accumulator
	start_signal = "assign node%s_st = "%(str(node["id"]))
	module_inline = ""
	for i in range(0,len(node["arguments"])):
		wire_line = "wire [%%BUS_WIDTH%%-1:0] %s;"%(str(node["arguments"][i]))
		if isinstance(node["arguments"][i], dict):
			wire_line = "wire [%%BUS_WIDTH%%-1:0] node%s_res;"%((str(node["arguments"][i]["id"]))) 
			rd_line = "wire node%s_rd;"%(str(node["arguments"][i]["id"]))
			start_signal = start_signal + "node%s_rd & "%(str(node["arguments"][i]["id"]))
			accumulator["wire"].extend([rd_line])
			module_inline = module_inline + "node%s_res, "%((str(node["arguments"][i]["id"])))
		else:
			module_inline = module_inline + "%s, "%(str(node["arguments"][i]))
		accumulator["wire"].extend([wire_line])
	start_signal = start_signal[:-3] + ";"
	if start_signal[-3:] == "st;":
		start_signal = start_signal[:-1] + " = ST;"
	module_inline = module_inline[:-2]
	start_wire = "node%s_st"%(str(node["id"]))
	ready_wire = "node%s_rd"%(str(node["id"]))
	res_wire  = "node%s_res"%(str(node["id"]))
	module_line = "node%s n%s(RST, %s, CLK, %s, %s, %s);"%(str(node["id"]), str(node["id"]), start_wire, ready_wire, res_wire, module_inline)
	accumulator["start"].extend([start_signal])
	accumulator["module"].extend([module_line])
	accumulator["wire"].extend(["wire %s;"%(start_wire)])
	return accumulator    

if __name__ == "__main__":
	line1 = "I(2,3;X,i(1;s(x),m(g(n),5)),Z)"
	line2 = "R(i(0;x,y),i(0;s(x),y);x,y)"
	line3 = "mul(x,y)"
	line4 = "R(i(0;x,y),i(0;s(x),y,z);x,y)"
	line5 = "add(x,y)"
	line6 = "add(x,mul(y,z))"
	tree = pparser.parseParentheses(line6)
	accumulator = {}
	accumulator["start"] = []
	accumulator["module"] = []
	accumulator["wire"] = ["wire [%d-1:0] node%s_res;"%(16, tree["id"])]
	graph = []
	acc,graph = treeWalk(tree, None, accumulator, graph, 16)
	drawGraph(graph, "root")
	(fl, tb) = generateRoot.generateRoot(tree, acc, 16)
	f = open("main_root.v",'w')
	f.write(fl)
	f.close()
	f = open("main_root_testbench.v",'w')
	f.write(tb)
	f.close()
