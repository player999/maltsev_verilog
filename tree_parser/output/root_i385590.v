module root_i385590(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_i385590_res;
	wire node_i385590_rd;
	wire node_i385590_st;

	assign RES = node_i385590_res;
	assign RD = node_i385590_rd;
	assign node_i385590_st = ST;


	node_i385590 n_i385590(RST,node_i385590_st,CLK,node_i385590_rd,node_i385590_res,IN0,IN1);
	
endmodule

