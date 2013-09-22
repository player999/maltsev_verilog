module root_i747374(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_s565034_res;
	wire [15:0] node_i747374_res;
	wire node_s565034_rd;
	wire node_s565034_st;
	wire node_i747374_rd;
	wire node_i747374_st;

	assign RES = node_i747374_res;
	assign RD = node_s565034_rd&node_i747374_rd;
	assign node_s565034_st = ST;
	assign node_i747374_st = node_s565034_rd;


	node_s565034 n_s565034(RST,node_s565034_st,CLK,node_s565034_rd,node_s565034_res,IN2);
	node_i747374 n_i747374(RST,node_i747374_st,CLK,node_i747374_rd,node_i747374_res,IN0,IN1,node_s565034_res);
	
endmodule

