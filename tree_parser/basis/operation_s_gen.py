#!/usr/bin/python3
from sys import argv
def generate_s(bw, node_id):
	template = open("operation_s.tmp", "r").read()
	template = template.replace("%BUS_WIDTH%", str(bw));
	template = template.replace("operation_s","node%s"%(node_id))
	out_file = open("node%s_operation_s.v"%(node_id),"w");
	out_file.write(template);
	out_file.close();
	
	template = open("operation_s_tb.tmp", "r").read()
	template = template.replace("%BUS_WIDTH%", str(bw));
	template = template.replace("operation_s","node%s"%(node_id))
	out_file = open("node%s_operation_s_tb.v"%(node_id),"w");
	out_file.write(template);
	out_file.close();

if __name__ == "__main__":
	bus_width = argv[1];
	generate_s(bus_width, node_id)
