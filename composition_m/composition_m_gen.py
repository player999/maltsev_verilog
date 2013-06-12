#!/usr/bin/python3.3
from sys import argv

if __name__ == "__main__":
	bus_width = argv[2];
	in_cnt = argv[3];
	func_f = argv[1];
	in_criterion = argv[4];
	
	in_list = ""
	in_def = ""
	inf_list = ""
	in_wire = ""
	in_register = ""
	in_assign = ""
	in_init = ""

	for i in range(0, int(in_cnt)):
		in_list += "IN%d, "%(i)
		in_def += "\tinput wire [%s-1:0] IN%d;\n"%(bus_width, i)
		if(i == int(in_criterion)):
			inf_list += "CNT, "
		else:
			inf_list += "IN%d, "%(i)
		in_wire += "\twire [%d:0] IN%d;\n"%(int(bus_width) - 1, i)
		in_register += "\treg [%d:0] rIN%d;\n"%(int(bus_width) - 1, i)
		in_assign += "\tassign IN%d = rIN%d;\n"%(i, i)
		in_init += "\t\trIN%d = %d;\n"%(i, i)

	
		
	in_list = in_list[0:-2]
	inf_list =  inf_list[0:-2]

	template = open("composition_m.tmp", "r").read()
	template = template.replace("%BUS_WIDTH", bus_width)
	template = template.replace("composition_m","composition_m_f%s_bw%s_icnt%s_crit%s"%(func_f, bus_width, in_cnt, in_criterion))
	template = template.replace("%IN_LIST", in_list)
	template = template.replace("%IN_DEF", in_def)
	template = template.replace("%INF_LIST", inf_list)
	template = template.replace("%F_CLASS", func_f)


	out_file = open("composition_m_f%s_bw%s_icnt%s_crit%s.v"%(func_f, bus_width, in_cnt, in_criterion),"w")
	out_file.write(template)
	out_file.close()

	template = open("composition_m_tb.tmp", "r").read()
	template = template.replace("%BUS_WIDTH", str(bus_width));
	template = template.replace("composition_m","composition_m_f%s_bw%s_icnt%s_crit%s"%(func_f, bus_width, in_cnt, in_criterion))
	template = template.replace("%IN_WIRE", in_wire);
	template = template.replace("%IN_REGISTER", in_register);
	template = template.replace("%IN_ASSIGN", in_assign);
	template = template.replace("%IN_INIT", in_init);
	template = template.replace("%IN_PARAM", in_list);


	out_file = open("composition_m_f%s_bw%s_icnt%s_crit%s_tb.v"%(func_f, bus_width, in_cnt, in_criterion),"w")
	out_file.write(template);
	out_file.close();
