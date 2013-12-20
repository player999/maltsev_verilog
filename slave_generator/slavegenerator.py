#!/usr/bin/python3
#-*-tab-width:4-*-
import argparse
import math

TEMPLATE="slave.tmp"


def generate_filling_if(bytenr, dw):
	line = ""
	line = line + "\t\t\t\t\tif(SEL_I[%i]) begin\n"%bytenr
	line = line + "\t\t\t\t\t\tcase(complete)\n"
	d1 = (bytenr + 1) * 8 - 1;
	d0 = bytenr * 8;
	for i in range(0, int(dw / 8)):
		r1 = (i + 1) * 8 - 1;
		r0 = i * 8;
		line = line + "\t\t\t\t\t\t\t%i: regs[adr][%i:%i] = DAT_I[%i:%i];\n"%(i, r1, r0, d1, d0)
	line = line + "\t\t\t\t\t\tendcase\n"
	line = line + "\t\t\t\t\t\tcomplete = complete + 1;\n"
	line = line + "\t\t\t\t\tend//END SEL_I[%i]\n"%bytenr
	return line

def create_slave(slavename, slaveid, modulename, incnt, dw, selbits):
	regs_line = ""
	for i in range(0,incnt):
		regs_line = regs_line + "regs[%i], "%i
	regs_line = regs_line[:-2]
	clear_modules=""
	for i in range(0,incnt):
		clear_modules = clear_modules + "\t\t\tregs[%i] = 0;\n"%i
	filling = ""
	for i in range(0,int(dw / 8)):
		filling = filling + generate_filling_if(int(dw / 8) - i - 1, dw)
	#Fill template
	template = open(TEMPLATE, "r").read()
	template = template.replace("%FILLING%", filling)
	template = template.replace("%DW%", str(dw))
	template = template.replace("%IN_CNT%", str(incnt))
	template = template.replace("%NSELBITS%", str(selbits))
	template = template.replace("%NADRBITS%", str(math.ceil(math.log2(incnt))))
	template = template.replace("%SLAVEID%", str(slaveid))
	template = template.replace("%MODULE_NAME%", slavename)
	template = template.replace("%INTERNAL_MODULE%", modulename)
	template = template.replace("%REGISTER_LINE%", regs_line)
	template = template.replace("%CLEAR_MODULES%", clear_modules)
	f = open(slavename + ".v", "w")
	f.write(template)
	f.close()
	return template
if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="slavegenerator")
	parser.add_argument("--incnt", type=int, required=True)
	parser.add_argument("--dw", type=int, default=32)
	parser.add_argument("--selbits", type=int, required=True)
	parser.add_argument("--slavename", type=str, default="slave")
	parser.add_argument("--slaveid", type=int, required=True)
	parser.add_argument("--modulename", type=str, required=True)
  
	args = parser.parse_args()
	
	create_slave(args.slavename, args.slaveid, args.modulename, args.incnt, args.dw, args.selbits)
	
