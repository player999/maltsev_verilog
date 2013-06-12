module composition_r_goperation_o_bw16_inc2_hmultiplication_func_h_bw_16_icnt2(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	output reg RD;
	output reg [16-1:0] RES;
	wire [16-1:0] res_g;
	wire [16-1:0] res_h;
	reg [16-1:0] CNT;
	reg [16-1:0] ITERATIONS;
	wire rd_g;
	wire rd_h;
	wire st_h;
	reg STold;
	reg rd_g_old;
	reg rd_h_old;
	
	input wire [16-1:0] IN0;
	input wire [16-1:0] IN1;

	wire [16-1:0] IN2;
	
	operation_o_bw16_inc2 g(RST, ST, CLK, rd_g, res_g, IN0, IN1);
	multiplication_func_h h(RST, st_h, CLK, rd_h, res_h, IN0, IN1, IN2);
	//g, h
	
	assign st_h = CNT?rd_h:rd_g;
	assign IN2[16-1:0] = (CNT[16-1:0] > 1)?res_h[16-1:0]:res_g[16-1:0];

	always @(posedge CLK) begin
		if(RST == 1) begin
			RD = 1;
			CNT = 0;
			STold = 0;
			rd_g_old = 0;
			rd_h_old = 0;
			ITERATIONS = 0;
		end else begin
			if(ITERATIONS == CNT) begin
				RD = 1;
				CNT = 0;
				RES = res_h;
				ITERATIONS = 0;
			end
			if(RD == 0) begin
				
				if(rd_g == 1 && rd_g_old == 0 && CNT == 0) begin
					RES = res_g;
					CNT = CNT + 1;
				end
				if(rd_h == 1 && rd_h_old == 0) begin
					RES = rd_h;
					CNT = CNT + 1;
				end
					
			end
			if(ST == 1 && STold == 0) begin
				RD = 0;
				ITERATIONS = IN1;
			end
		end
		STold = ST;
		rd_g_old = rd_g;
		rd_h_old = rd_h;
	end
endmodule
