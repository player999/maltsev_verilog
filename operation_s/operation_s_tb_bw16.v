module operation_s_16_tb;
	wire CLK;
	reg rCLK;
	wire RST;
	reg rRST;
	wire ST;
	reg rST;
	wire RD;
	wire [16-1:0] RES;
	wire [16-1:0] IN;
	reg [16-1:0] rIN;
	
	operation_s_16 op_s(RST, ST, CLK, RD, RES, IN);

	assign CLK = rCLK;
	assign ST = rST;
	assign RST = rRST;
	assign IN = rIN;

	initial begin
		$dumpfile("operation_s_16_tb.vcd");
		$dumpvars;
		rCLK = 0;
		rRST = 1;
		rST = 0;
		rIN = 2;
		#15 rRST = 0;
		#10 rST = 1;
		#40 $finish;
	end


	always #5 rCLK = !rCLK;
	
endmodule
