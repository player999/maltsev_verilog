module multiplication_tb;
	wire CLK;
	reg rCLK;
	wire RST;
	reg rRST;
	wire ST;
	reg rST;
	wire RD;
	wire [16-1:0] RES;
	wire [15:0] IN0;
	wire [15:0] IN1;

	reg [15:0] rIN0;
	reg [15:0] rIN1;
	
	composition_r_goperation_o_bw16_inc2_hmultiplication_func_h_bw_16_icnt2 op_m(RST, ST, CLK, RD, RES, IN0, IN1);

	assign CLK = rCLK;
	assign ST = rST;
	assign RST = rRST;
	assign IN0 = rIN0;
	assign IN1 = rIN1;

	initial begin
		$dumpfile("addition_tb.vcd");
		$dumpvars;
		rCLK = 0;
		rRST = 1;
		rST = 0;
		rIN0 = 4;
		rIN1 = 5;
		#15 rRST = 0;
		#10 rST = 1;
		#10 rST = 0;
		#4000 $finish;
	end


	always #5 rCLK = !rCLK;
	
endmodule
