module root_i758168(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_i758168_res;
	wire node_i758168_rd;
	wire node_i758168_st;

	assign RES = node_i758168_res;
	assign RD = node_i758168_rd;
	assign node_i758168_st = ST;


	node_i758168 n_i758168(RST,node_i758168_st,CLK,node_i758168_rd,node_i758168_res,IN0,IN1);
	
endmodule

