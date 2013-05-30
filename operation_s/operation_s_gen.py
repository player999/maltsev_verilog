#!/usr/bin/python3.3
from sys import argv

if __name__ == "__main__":
	bus_width = argv[1];
		
	template = open("operation_s.tmp", "r").read()
	template = template.replace("%BUS_WIDTH", str(bus_width));
	template = template.replace("operation_s","operation_s_bw%s"%(bus_width))
	out_file = open("operation_s_bw%s.v"%(bus_width),"w");
	out_file.write(template);
	out_file.close();
	
	template = open("operation_s_tb.tmp", "r").read()
	template = template.replace("%BUS_WIDTH", str(bus_width));
	template = template.replace("operation_s","operation_s_%s"%(bus_width))
	out_file = open("operation_s_tb_bw%s.v"%(bus_width),"w");
	out_file.write(template);
	out_file.close();

