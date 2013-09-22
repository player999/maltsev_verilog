module root_i176191(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_i176191_res;
	wire node_i176191_rd;
	wire node_i176191_st;

	assign RES = node_i176191_res;
	assign RD = node_i176191_rd;
	assign node_i176191_st = ST;


	node_i176191 n_i176191(RST,node_i176191_st,CLK,node_i176191_rd,node_i176191_res,IN0,IN1);
	
endmodule

