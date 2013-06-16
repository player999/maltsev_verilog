#!/usr/bin/python3.2
from sys import argv

def generate_o(bus_width, input_count, node_id="0"):
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
        in_init += "\t\trIN%d = 4;\n"%(i)
	
    in_list = in_list[0:-2]
		
    template = open("operation_o.tmp", "r").read()
    template = template.replace("%IN", in_list);
    template = template.replace("%IDEF", idef);
    template = template.replace("%BUS_WIDTH", str(bus_width));
    template = template.replace("operation_o","node%s"%(node_id))
    out_file = open("node%s_operation_o.v"%(node_id),"w");
    out_file.write(template);
    out_file.close();
	
    template = open("operation_o_tb.tmp", "r").read()
    template = template.replace("%BUS_WIDTH", str(bus_width));
    template = template.replace("operation_o","node%s"%(node_id))
    template = template.replace("%IN_WIRE", in_wire);
    template = template.replace("%IN_REGISTER", in_register);
    template = template.replace("%IN_ASSIGN", in_assign);
    template = template.replace("%IN_INIT", in_init);
    template = template.replace("%IN_PARAM", in_list);


    out_file = open("node%s_tb.v"%(node_id),"w");
    out_file.write(template);
    out_file.close();

if __name__ == "__main__":
    bus_width = argv[1];
    input_count = argv[2];
    generate_o(bus_width, input_count)	

