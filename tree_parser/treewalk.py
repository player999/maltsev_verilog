#!/usr/bin/python3
import pparser
import generateRoot
import operation_o_gen

def treeWalk(tree, parentNode, accumulator, bw):
    accumulator = generateAccEntry(tree, accumulator, bw)
    generateNode(tree, bw)
    for leaf in tree["arguments"]:
        if isinstance(leaf, dict):
            accumulator = treeWalk(leaf, tree, accumulator, bw)
    return accumulator

def generateNode(node, bw):
    if node["name"] == "":
        print("d")
    else:
        operation_o_gen.generate_o(bw, len(node["arguments"]), node["id"])

def generateAccEntry(node, accumulator, bw):
    if isinstance(node, str):
        return accumulator
    start_signal = "assign node%s_st = "%(str(node["id"]))
    module_inline = ""
    for i in range(0,len(node["arguments"])):
        wire_line = "wire [%%BUS_WIDTH%%-1:0] node%s_in%d;"%(str(node["id"]), i)
        if isinstance(node["arguments"][i], dict):
            wire_line = "wire [%%BUS_WIDTH%%-1:0] node%s_res;"%((str(node["arguments"][i]["id"]))) 
            rd_line = "wire node%s_rd;"%(str(node["arguments"][i]["id"]))
            start_signal = start_signal + "node%s_rd & "%(str(node["arguments"][i]["id"]))
            accumulator["wire"].extend([rd_line])
            module_inline = module_inline + "node%s_res, "%((str(node["arguments"][i]["id"])))
        else:
            module_inline = module_inline + "node%s_in%d, "%(str(node["id"]), i)
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
    line = "I(2,3;X,add(s(x), m(g(n), 5)),Z)"
    tree = pparser.parseParentheses(line)
    accumulator = {}
    accumulator["start"] = []
    accumulator["module"] = []
    accumulator["wire"] = ["wire [%d-1:0] node%s_res;"%(16, tree["id"])]
    acc = treeWalk(tree, None, accumulator, 16)
    (fl, tb) = generateRoot.generateRoot(tree, acc, 16)
    f = open("main_root.v",'w')
    f.write(fl)
    f.close()
    f = open("main_root_tb.v",'w')
    f.write(tb)
    f.close()