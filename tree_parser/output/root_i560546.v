module root_i560546(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_s563208_res;
	wire [15:0] node_i560546_res;
	wire node_s563208_rd;
	wire node_s563208_st;
	wire node_i560546_rd;
	wire node_i560546_st;

	assign RES = node_i560546_res;
	assign RD = node_s563208_rd&node_i560546_rd;
	assign node_s563208_st = ST;
	assign node_i560546_st = node_s563208_rd;


	node_s563208 n_s563208(RST,node_s563208_st,CLK,node_s563208_rd,node_s563208_res,IN2);
	node_i560546 n_i560546(RST,node_i560546_st,CLK,node_i560546_rd,node_i560546_res,IN0,IN1,node_s563208_res);
	
endmodule

