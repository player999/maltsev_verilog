module root_i911139(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_i911139_res;
	wire node_i911139_rd;
	wire node_i911139_st;

	assign RES = node_i911139_res;
	assign RD = node_i911139_rd;
	assign node_i911139_st = ST;


	node_i911139 n_i911139(RST,node_i911139_st,CLK,node_i911139_rd,node_i911139_res,IN0,IN1);
	
endmodule

