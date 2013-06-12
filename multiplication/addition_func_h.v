module addition_func_h(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	output wire RD;
	output wire [15:0] RES;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	wire [15:0] RESi;
	wire  RDi;
	
	operation_i_bw16_inc3_si2 opi3(RST, ST, CLK, RDi, RESi, IN0, IN1, IN2);
	operation_s_bw16 soperation(RST, RDi, CLK, RD, RES, RESi);	
	
endmodule
