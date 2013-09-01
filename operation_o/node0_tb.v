module node0_tb;
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
	wire [15:0] IN2;

	reg [15:0] rIN0;
	reg [15:0] rIN1;
	reg [15:0] rIN2;

	
	node0 op_o(RST, ST, CLK, RD, RES, IN0, IN1, IN2);

	assign CLK = rCLK;
	assign ST = rST;
	assign RST = rRST;
	assign IN0 = rIN0;
	assign IN1 = rIN1;
	assign IN2 = rIN2;


	initial begin
		$dumpfile("node0_tb.vcd");
		$dumpvars;
		rCLK = 0;
		rRST = 1;
		rST = 0;
		rIN0 = 4;
		rIN1 = 4;
		rIN2 = 4;

		#15 rRST = 0;
		#10 rST = 1;
		#10 rST = 0;
		#10 $finish;
	end


	always #5 rCLK = !rCLK;
	
endmodule
