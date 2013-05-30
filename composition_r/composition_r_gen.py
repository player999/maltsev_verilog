#!/usr/bin/python3.3
from sys import argv

if __name__ == "__main__":
	bus_width = argv[1];
	in_cnt = argv[2];
	func_g = argv[3];
	func_h = argv[4];
	
	in_list = ""
	in_def = ""
	print(int(in_cnt))
	for i in range(0, int(in_cnt)):
		in_list += "IN%d, "%(i)
		in_def += "\tinput wire [%s-1:0] IN%d;\n"%(bus_width, i)
		
	in_list = in_list[0:-2]
	max_in = int(in_cnt) - 1

	template = open("composition_r.tmp", "r").read()
	template = template.replace("%BUS_WIDTH", bus_width)
	template = template.replace("composition_r","composition_r_g%s_h%s_bw_%s_icnt%s"%(func_g, func_h, bus_width, in_cnt))
	template = template.replace("%IN_LIST", in_list)
	template = template.replace("%IN_DEF", in_def)
	template = template.replace("%G_CLASS", func_g)
	template = template.replace("%H_CLASS", func_h);
	template = template.replace("%MAX_IN", "IN%d"%(max_in))

	out_file = open("composition_r_g%s_h%s_bw_%s_icnt%s.v"%(func_g, func_h, bus_width, in_cnt),"w")
	out_file.write(template)
	out_file.close()
	
	#template = open("operation_s_tb.tmp", "r").read()
	#template = template.replace("%BUS_WIDTH", str(bus_width));
	#template = template.replace("operation_s","operation_s_%s"%(bus_width))
	#out_file = open("operation_s_tb_bw%s.v"%(bus_width),"w");
	#out_file.write(template);
	#out_file.close();

