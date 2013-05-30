#!/usr/bin/python3.3
from sys import argv

if __name__ == "__main__":
	bus_width = argv[1];
	input_count = argv[2];
	selected_input = argv[3];
	in_list = ""
	idef = ""
	in_wire = ""
	in_register = ""
	in_assign = ""
	in_init = ""
	for i in range(0,int(input_count)):
		in_list += "IN%d, "%(i)
		idef += "\tinput wire [%d:0] IN%d;\n"%(int(bus_width) - 1, i)
		in_wire += "\twire [%d:0] IN%d;\n"%(int(bus_width) - 1, i)
		in_register += "\treg [%d:0] rIN%d;\n"%(int(bus_width) - 1, i)
		in_assign += "\tassign IN%d = rIN%d;\n"%(i, i)
		in_init += "\t\trIN%d = %d;\n"%(i, i)
		 
	in_list = in_list[0:-2]
		
	template = open("operation_i.tmp", "r").read()
	template = template.replace("%IN", in_list);
	template = template.replace("%IDEF", idef);
	template = template.replace("%IRESULT", "IN%s"%(selected_input));
	template = template.replace("%BUS_WIDTH", str(bus_width));
	template = template.replace("operation_i","operation_i_bw%s_inc%s_si%s"%(bus_width, input_count, selected_input))
	out_file = open("operation_i_bw%s_inc%s_si%s.v"%(bus_width, input_count, selected_input),"w");
	out_file.write(template);
	out_file.close();
	
	template = open("operation_i_tb.tmp", "r").read()
	template = template.replace("%BUS_WIDTH", str(bus_width));
	template = template.replace("operation_i","operation_i_bw%s_inc%s_si%s"%(bus_width, input_count, selected_input))
	template = template.replace("%IN_WIRE", in_wire);
	template = template.replace("%IN_REGISTER", in_register);
	template = template.replace("%IN_ASSIGN", in_assign);
	template = template.replace("%IN_INIT", in_init);
	template = template.replace("%IN_PARAM", in_list);


	out_file = open("operation_i_tb_bw%s_inc%s_si%s.v"%(bus_width, input_count, selected_input),"w");
	out_file.write(template);
	out_file.close();

