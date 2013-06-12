module multiplication_func_h(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	output wire RD;
	output wire [15:0] RES;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;
	
	composition_r_goperation_i_bw16_inc2_si1_haddition_func_h_bw_16_icnt2 summa(RST, ST, CLK, RD, RES, IN0, IN2);	
	
endmodule
