#!/usr/bin/python3
from sys import argv

def generate_r(bus_width, inputs, func_g, func_h, node_id):
	in_list = ""
	in_def = ""
	print(inputs)
	for i in range(0, len(inputs)-1):
		in_list += "%s, "%(inputs[i])
		in_def += "\tinput wire [%s-1:0] %s;\n"%(str(bus_width), inputs[i])		
	in_list = in_list[0:-2]
	max_in = len(inputs)
	template = open("composition_r.tmp", "r").read()
	template = template.replace("%BUS_WIDTH%", str(bus_width))
	template = template.replace("composition_r","node%s"%(node_id))
	template = template.replace("%IN_LIST%", in_list)
	template = template.replace("%IN_DEF%", in_def)
	template = template.replace("%G_CLASS%", "root"+func_g)
	template = template.replace("%H_CLASS%", "root"+func_h);
	template = template.replace("%MAX_IN%", "%s"%(inputs[-2]))
	template = template.replace("%ADDITIONAL_IN%", "%s"%(inputs[-1]))

	out_file = open("node%s_composition_r.v"%(node_id),"w")
	out_file.write(template)
	out_file.close()

if __name__ == "__main__":
	bus_width = argv[1];
	in_cnt = argv[2];
	func_g = argv[3];
	func_h = argv[4];
	
	generate_r(int(bus_width), in_cnt, func_g, func_h, "0")
