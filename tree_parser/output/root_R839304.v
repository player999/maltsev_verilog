module root_R839304(RST, ST, CLK, RD, RES, IN0, IN1, IN2, IN3, IN4);
	input wire RST;
	input wire ST;
	input wire CLK;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	input wire [15:0] IN3;
	input wire [15:0] IN4;
	output wire RD;
	output wire [15:0] RES;
	


	wire [15:0] node_R971708_res;
	wire [15:0] node_R342462_res;
	wire [15:0] node_R105807_res;
	wire [15:0] node_R839304_res;
	wire node_R971708_rd;
	wire node_R971708_st;
	wire node_R342462_rd;
	wire node_R342462_st;
	wire node_R105807_rd;
	wire node_R105807_st;
	wire node_R839304_rd;
	wire node_R839304_st;

	assign RES = node_R839304_res;
	assign RD = node_R971708_rd&node_R342462_rd&node_R105807_rd&node_R839304_rd;
	assign node_R971708_st = ST;
	assign node_R342462_st = node_R971708_rd;
	assign node_R105807_st = ST;
	assign node_R839304_st = node_R342462_rd&node_R105807_rd;


	node_R971708 n_R971708(RST,node_R971708_st,CLK,node_R971708_rd,node_R971708_res,IN0,IN1);
	node_R342462 n_R342462(RST,node_R342462_st,CLK,node_R342462_rd,node_R342462_res,node_R971708_res,IN2);
	node_R105807 n_R105807(RST,node_R105807_st,CLK,node_R105807_rd,node_R105807_res,IN3,IN4);
	node_R839304 n_R839304(RST,node_R839304_st,CLK,node_R839304_rd,node_R839304_res,node_R342462_res,node_R105807_res);
	
endmodule

