module root_i986560(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_s938797_res;
	wire [15:0] node_i986560_res;
	wire node_s938797_rd;
	wire node_s938797_st;
	wire node_i986560_rd;
	wire node_i986560_st;

	assign RES = node_i986560_res;
	assign RD = node_s938797_rd&node_i986560_rd;
	assign node_s938797_st = ST;
	assign node_i986560_st = node_s938797_rd;


	node_s938797 n_s938797(RST,node_s938797_st,CLK,node_s938797_rd,node_s938797_res,IN2);
	node_i986560 n_i986560(RST,node_i986560_st,CLK,node_i986560_rd,node_i986560_res,IN0,IN1,node_s938797_res);
	
endmodule

