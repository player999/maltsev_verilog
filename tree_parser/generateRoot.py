#!/usr/bin/python3
import re

def isWireType(tpe, line):
    res = re.findall("^wire.*_(.*);", line)
    res = res[0][:2]
    if res == tpe:
        return 1
    else:
        return 0

def extractWireName(line):
    res = re.findall("^wire \[.*?\] (.*);", line)
    res = res[0]
    return res

def generateRoot(tree, acc, bw):
    template = open("root.tmp", "r").read()
    template = template.replace("%ROOT_NODE_ID%", tree["id"]);
    input_definitions = ""
    inputs = ""
    wires = ""
    for arg in acc["wire"]:
        if isWireType("in", arg):
            input_definitions = input_definitions + "    input %s\n"%(arg)
            inputs = inputs + "%s, "%extractWireName(arg)
        else:
            wires = wires + "    %s\n"%(arg)
    inputs = inputs[:-2] 
    template = template.replace("%IN%", inputs);
    template = template.replace("%INPUT_DEFINITIONS%", input_definitions)
    
    modules = ""
    for modline in acc["module"]:
        modules = modules + "    %s\n"%(modline)
    template = template.replace("%MODULES%", modules)

    assignments = ""
    for ass in acc["start"]:
        assignments = assignments + "    %s\n"%(ass)
    assignments = assignments + "    assign RD = node%s_rd;\n"%(tree["id"])
    assignments = assignments + "    assign RES[%d:0] = node%s_res[%d:0];\n"%(int(bw)-1, tree["id"], int(bw)-1)
    template = template.replace("%ASSIGNMENTS%", assignments)
    template = template.replace("%WIRES%", wires)
    template = template.replace("%BUS_WIDTH%", str(bw))
    #Generate testbench
    template_tb = open("root_tb.tmp", "r").read()
    input_wires = ""
    input_regs = ""
    assign_wires = ""
    in_init = ""
    cnt = 5
    for arg in acc["wire"]:
        if isWireType("in", arg):
            wire = re.findall("^.*(node.*);", arg)
            wire = wire[0]
            input_wires = input_wires + "\twire [%d-1:0] %s;\n"%(bw, wire)
            input_regs = input_regs + "\treg [%d-1:0] r%s;\n"%(bw, wire) 
            assign_wires = assign_wires + "\tassign %s = r%s;\n"%(wire, wire)
            in_init = in_init + "\tr%s = %d;\n"%(wire, cnt)
            cnt = cnt + 1
    
    template_tb = template_tb.replace("%INDEF%", input_wires + input_regs)
    template_tb = template_tb.replace("%ROOT_NODE_ID%", tree["id"])
    template_tb = template_tb.replace("%IN%", inputs)
    template_tb = template_tb.replace("%IN_ASSIGN%", assign_wires)
    template_tb = template_tb.replace("%SIM_TIME%", str(3000))
    template_tb = template_tb.replace("%IN_INIT%", in_init)    
    template_tb = template_tb.replace("%BUS_WIDTH%", str(bw))
    return template, template_tb
    
     
