module composition_m_foperation_i_bw16_inc3_si2_bw16_icnt3_crit2(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	output reg RD;
	output reg [16-1:0] RES;
	wire [16-1:0] res_f;
	reg [16-1:0] CNT;
	wire rd_f;
	reg st_f;
	reg stf_f;
	reg RDold_f;
	reg STold;
	reg [16-1:0] INv;
	input wire [16-1:0] IN0;
	input wire [16-1:0] IN1;
	input wire [16-1:0] IN2;

	operation_i_bw16_inc3_si2 f(RST, st_f, CLK, rd_f, res_f, IN0, IN1, CNT);
	
	always @(posedge CLK) begin
		if(RST == 1) begin
			RD = 1;
			STold = 0;
			CNT = 0;
			stf_f = 0;
		end else begin
			if(stf_f == 1) begin
				stf_f = 0;
				st_f = 0;
			end
			if(st_f == 1) begin
				stf_f = 1;
			end	
			if(ST == 1 && STold == 0) begin
				CNT = 0;
				RD = 0;
				st_f = 1;				
			end

			if(RDold_f == 0 && rd_f == 1) begin
				if(res_f == 0) begin
					RD = 1;
					RES = res_f;
				end
				CNT = CNT + 1;
				st_f = 1;
			end
		end
		STold = ST;
		RDold_f = rd_f;
	end
endmodule
