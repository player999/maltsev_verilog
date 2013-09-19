#!/usr/bin/python3
from sys import argv
def generate_i(bw, ic, si, node_id="0"):
	in_list = ""
	idef = ""
	in_wire = ""
	in_register = ""
	in_assign = ""
	in_init = ""
	for i in range(0,int(ic)):
		in_list += "in%d, "%(i)
		idef += "\tinput wire [%d:0] in%d;\n"%(int(bw) - 1, i)
		in_wire += "\twire [%d:0] in%d;\n"%(int(bw) - 1, i)
		in_register += "\treg [%d:0] rin%d;\n"%(int(bw) - 1, i)
		in_assign += "\tassign in%d = rin%d;\n"%(i, i)
		in_init += "\t\trin%d = %d;\n"%(i, i)
		 
	in_list = in_list[0:-2]
		
	template = open("operation_i.tmp", "r").read()
	template = template.replace("%IN%", in_list);
	template = template.replace("%IDEF%", idef);
	template = template.replace("%IRESULT%", "in%s"%(si));
	template = template.replace("%BUS_WIDTH%", str(bw));
	template = template.replace("operation_i","node%s"%(node_id))
	out_file = open("node%s_operation_i.v"%(node_id),"w");
	out_file.write(template);
	out_file.close();
	
	template = open("operation_i_tb.tmp", "r").read()
	template = template.replace("%BUS_WIDTH%", str(bw));
	template = template.replace("operation_i","node%s"%(node_id))
	template = template.replace("%IN_WIRE%", in_wire);
	template = template.replace("%IN_REGISTER%", in_register);
	template = template.replace("%IN_ASSIGN%", in_assign);
	template = template.replace("%IN_INIT%", in_init);
	template = template.replace("%in_param%", in_list);


	out_file = open("node%s_operation_i_tb.v"%(node_id),"w");
	out_file.write(template);
	out_file.close();

if __name__ == "__main__":
	bw = argv[1];
	input_count = argv[2];
	selected_input = argv[3];
	generate_i(bw, input_count, selected_input)	
