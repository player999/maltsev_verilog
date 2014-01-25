module fortestbench();
   wire RST;
   reg 	rRST;
   wire CLK;
   reg 	rCLK;
   wire ST;
   reg 	rST;
   wire [16-1:0] IN1;
   wire [16-1:0] IN2;
   wire [16-1:0] IN3;
   reg [16-1:0]  rIN1;
   reg [16-1:0]  rIN2;
   reg [16-1:0]  rIN3;
   wire [16-1:0] RES;
   wire 		 RD;
   
   assign RST = rRST;
   assign ST = rST;
   assign CLK = rCLK;
   assign IN1 = rIN1;
   assign IN2 = rIN2;
   assign IN3 = rIN3;
   
   modulename dut(RST, ST, CLK, RD, RES, IN1, IN2, IN3);
   
   initial rCLK = 0;
   always #5 rCLK = ~rCLK;
   
   initial begin
	  $dumpfile("result.vcd");
	  $dumpvars;
	  rIN1 = 5;
	  rIN2 = 4;
	  rIN3 = 3;
	  rRST = 1;
	  #20 rRST = 0;
	  rST = 1;
	  #20 rST = 0;
	  #2000
	  $finish;
   end
 
   
endmodule // fortestbench
