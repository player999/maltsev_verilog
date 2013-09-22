module root_i115175(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_R830051_res;
	wire [15:0] node_i115175_res;
	wire node_R830051_rd;
	wire node_R830051_st;
	wire node_i115175_rd;
	wire node_i115175_st;

	assign RES = node_i115175_res;
	assign RD = node_R830051_rd&node_i115175_rd;
	assign node_R830051_st = ST;
	assign node_i115175_st = node_R830051_rd;


	node_R830051 n_R830051(RST,node_R830051_st,CLK,node_R830051_rd,node_R830051_res,IN2,IN0);
	node_i115175 n_i115175(RST,node_i115175_st,CLK,node_i115175_rd,node_i115175_res,IN0,IN1,node_R830051_res);
	
endmodule

