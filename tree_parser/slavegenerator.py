#!/usr/bin/python3
#-*-tab-width:4-*-
import argparse
import math
import glob
from configs import *

TEMPLATE=PLATFORM + "/slave_avalon.tmp"
TCL_TEMPLATE=PLATFORM + "/accelerator_tcl.tmp"
AUTHOR_NAME="Taras Zakharchenko"

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

def create_slave(slavename, path, modulename, incnt, dw):
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
	template = template.replace("%NSELBITS%", str(int(dw/8)))
	template = template.replace("%NADRBITS%", str(math.ceil(math.log2(incnt))))
	template = template.replace("%MODULE_NAME%", slavename)
	template = template.replace("%INTERNAL_MODULE%", modulename)
	template = template.replace("%REGISTER_LINE%", regs_line)
	template = template.replace("%CLEAR_MODULES%", clear_modules)
	f = open(path + "/" + slavename + ".v", "w")
	f.write(template)
	f.close()
	return template

def file_entry(path, name):
	line = "add_fileset_file %s VERILOG PATH %s\n"%(name, "./" + name)
	return line

def create_tcl(slavename, path, modulename, dw):
	#%BW% %TOP_LEVEL_PATH% %ACCELERATOR_NAME% %ACCELERATOR_DNAME% %AUTHOR_NAME% 
	TOP_LEVEL_PATH = "./" + slavename + ".v"
	BW = dw
	ACCELERATOR_NAME = slavename
	ACCELERATOR_DNAME = (" ").join(slavename.split("_"))
	FILE_LIST = ""
	file_list = glob.glob(path + "/*.v")
	for i in range(0, len(file_list)):
		file_list[i] = file_list[i].split("/")[-1]
		if "accelerator_" != file_list[i][:12] and "root_tb" != file_list[i][:7]:
			FILE_LIST = FILE_LIST + file_entry(path, file_list[i])
	template = open(TCL_TEMPLATE, "r").read()
	template = template.replace("%TOP_LEVEL_PATH%", TOP_LEVEL_PATH)
	template = template.replace("%BW%", str(dw))
	template = template.replace("%ACCELERATOR_NAME%", ACCELERATOR_NAME)
	template = template.replace("%ACCELERATOR_DNAME%", ACCELERATOR_DNAME)
	template = template.replace("%AUTHOR_NAME%", AUTHOR_NAME)
	template = template.replace("%FILE_LIST%", FILE_LIST)
	f = open(path + "/" + slavename + "_hw.tcl", "w")
	f.write(template)
	f.close()
	return

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="slavegenerator")
	parser.add_argument("--incnt", type=int, required=True)
	parser.add_argument("--dw", type=int, default=32)
	parser.add_argument("--modulename", type=str, required=True)
	parser.add_argument("--filename", type=str, default="slave")
	parser.add_argument("--path", type=str, required=True)
  
	args = parser.parse_args()
	create_tcl(args.filename, args.path, args.modulename, args.dw)
	create_slave(args.filename, args.path, args.modulename, args.incnt, args.dw)

	
