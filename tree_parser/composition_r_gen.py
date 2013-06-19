#!/usr/bin/python3
from sys import argv

def generate_r(bus_width, in_cnt, func_g, func_h, node_id):
	in_list = ""
	in_def = ""
	print(int(in_cnt))
	for i in range(0, int(in_cnt)):
		in_list += "IN%d, "%(i)
		in_def += "\tinput wire [%s-1:0] IN%d;\n"%(str(bus_width), i)
		
	in_list = in_list[0:-2]
	max_in = int(in_cnt)

	template = open("composition_r.tmp", "r").read()
	template = template.replace("%BUS_WIDTH%", str(bus_width))
	template = template.replace("composition_r","node%s"%(node_id))
	template = template.replace("%IN_LIST%", in_list)
	template = template.replace("%IN_DEF%", in_def)
	template = template.replace("%G_CLASS%", "root"+func_g)
	template = template.replace("%H_CLASS%", "root"+func_h);
	template = template.replace("%MAX_IN%", "IN%d"%(max_in-1))

	out_file = open("node%s_composition_r.v"%(node_id),"w")
	out_file.write(template)
	out_file.close()

if __name__ == "__main__":
	bus_width = argv[1];
	in_cnt = argv[2];
	func_g = argv[3];
	func_h = argv[4];
	
	generate_r(int(bus_width), in_cnt, func_g, func_h, "0")
