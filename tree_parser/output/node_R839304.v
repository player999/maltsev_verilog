module node_R839304(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	output reg RD;
	output reg [15:0] RES;
	reg [15:0] BUF;
	wire [15:0] res_g;
	wire [15:0] res_h;
	reg [15:0] CNT;
	reg [15:0] ITERATIONS;
	wire rd_g;
	wire rd_h;
	wire STst;
	reg st_h;
	reg st_h_f;
	reg STold;
	reg rd_g_old;
	reg rd_h_old;
	
input wire [15:0] IN0;
input wire [15:0] IN1;

	wire [15:0] IN2;

	starter strtr1(RST, CLK, ST, STst);	
	root_i758168 g(RST, STst, CLK, rd_g, res_g, IN0, IN1);
	root_i183247 h(RST, st_h, CLK, rd_h, res_h, IN0, IN1, IN2);
	//g, h
	
	assign IN2[15:0] = (CNT[15:0] > 1)?res_h[15-1:0]:res_g[15:0];

	always @(posedge CLK) begin
		if(RST == 1) begin
			RD = 1;
			CNT = 0;
			STold = 0;
			rd_g_old = 0;
			rd_h_old = 0;
			st_h_f = 0;
			st_h = 0;
		end else begin
			if(ITERATIONS == CNT & rd_g == 1) begin
				RD = 1;
				CNT = 0;
				st_h = 0;
				st_h_f = 0;
				if(ITERATIONS == 0) begin
					RES = res_g;
				end else begin
					RES = BUF;
				end
			end
			if(RD == 0) begin
				if(st_h_f == 0) begin
					st_h = 0;
				end
				if(st_h == 1) begin
					st_h_f = 0;
				end
				if(rd_g == 1 && rd_g_old == 0 && CNT == 0) begin
					BUF = res_g;
					st_h_f = 1;
					st_h = 1;
				end
				if(rd_h == 1 && rd_h_old == 0) begin
					BUF = res_h;
					CNT = CNT + 1;
					st_h_f = 1;
					st_h = 1;
				end
					
			end
			if(STst == 1 && STold == 0) begin
				RD = 0;
				if(IN1 > 0) begin
					ITERATIONS = IN1 + 2;
				end else begin
					ITERATIONS = 0;
				end
			end
		end
		if(STst == 1) begin
			STold = 1;
		end else begin
			STold = 0;
		end
		rd_g_old = rd_g;
		rd_h_old = rd_h;
	end
endmodule
