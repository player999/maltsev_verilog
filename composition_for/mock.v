module mock(RST, ST, CLK, RD, RES, IN1, IN2, IN3);
   input wire RST;
   input wire ST;
   input wire CLK;
   output reg RD;
   output reg [16-1:0] RES;
   input wire [16-1:0] IN1;
   input wire [16-1:0] IN2;
   input wire [16-1:0] IN3;
   reg [3:0] 		   CNT;
   
   always @(posedge CLK) begin
	  if(RST == 1) begin
		 RD = 1;
		 RES = 0;
		 CNT = 0;
	  end else begin
		 if (ST == 1 && RD == 1) begin
			RD = 0;
			CNT = 4;			
		 end else if (CNT > 0) begin
			CNT = CNT - 1;
		 end else begin
			RD = 1;
		 end
		 RES = IN2 - 1;
	  end
	  
	  
   end
   
			  

endmodule // mock
	 