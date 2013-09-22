module root_i183247(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_s777386_res;
	wire [15:0] node_i183247_res;
	wire node_s777386_rd;
	wire node_s777386_st;
	wire node_i183247_rd;
	wire node_i183247_st;

	assign RES = node_i183247_res;
	assign RD = node_s777386_rd&node_i183247_rd;
	assign node_s777386_st = ST;
	assign node_i183247_st = node_s777386_rd;


	node_s777386 n_s777386(RST,node_s777386_st,CLK,node_s777386_rd,node_s777386_res,IN2);
	node_i183247 n_i183247(RST,node_i183247_st,CLK,node_i183247_rd,node_i183247_res,IN0,IN1,node_s777386_res);
	
endmodule

