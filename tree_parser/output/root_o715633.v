module root_o715633(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_o715633_res;
	wire node_o715633_rd;
	wire node_o715633_st;

	assign RES = node_o715633_res;
	assign RD = node_o715633_rd;
	assign node_o715633_st = ST;


	node_o715633 n_o715633(RST,node_o715633_st,CLK,node_o715633_rd,node_o715633_res,IN0,IN1);
	
endmodule

