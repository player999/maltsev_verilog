module modulename(
				  RST, 
				  ST,
				  CLK,
				  RD,
				  RES,
				  IN1,
				  IN2,
				  IN3
				  );
   input wire RST;
   input wire ST;
   input wire CLK;
   output reg RD;
   output reg [16-1:0] RES;
   input wire [16-1:0] IN1;
   input wire [16-1:0] IN2;
   input wire [16-1:0] IN3;
   reg [16-1:0] 	   rIN1;
   reg [16-1:0] 	   rIN2;
   reg [16-1:0] 	   rIN3;
   reg [3:0] 		   state;
   reg [16-1:0] 	   rSOUT1;
   reg [16-1:0] 	   rSOUT2;
   reg [16-1:0] 	   rSOUT3;
   wire [16-1:0] 	   SOUT1;
   wire [16-1:0] 	   SOUT2;
   wire [16-1:0] 	   SOUT3;
   wire [16-1:0] 	   pRES;
   wire 			   RD1;
   wire 			   RD2;
   wire 			   RD3;
   wire 			   pRD;
   wire 			   lRD;
   reg 				   ST1;
   reg 				   ST2;
   reg 				   ST3;
   reg  			   pST;

   assign lRD = RD1 & RD2 & RD3;

   always @(posedge CLK) begin
	  if(RST == 1) begin
		 state = 0;
		 rSOUT1 = 0;
		 rSOUT2 = 0;
		 rSOUT3 = 0;
		 RD = 0;
		 RES = 0;
		 ST1 = 0;
		 ST2 = 0;
		 ST3 = 0;
		 pST = 0;
		 rIN1 = IN1;
		 rIN2 = IN2;
		 rIN3 = IN3;
	  end //Reset

	  case (state)
		0: begin 
		   state = 0;
		   rSOUT1 = 0;
		   rSOUT2 = 0;
		   rSOUT3 = 0;
		   rIN1 = IN1;
		   rIN2 = IN2;
		   rIN3 = IN3;
		   RD = 1;
		   RES = 0;
		   ST1 = 0;
		   ST2 = 0;
		   ST3 = 0;
		   pST = 0;
		   if (ST == 1) state = 1;
		end
		1: begin
		   RD = 0;
		   ST1 = 1;
		   ST2 = 1;
		   ST3 = 1;
		   state = 2;
		end
		2: begin
		   state = 3;
		end
		3: begin
		   ST1 = 0;
		   ST2 = 0;
		   ST3 = 0;
		   if (lRD == 1) state = 4;
		end
		4: begin
		   rSOUT1 = SOUT1;
		   rSOUT2 = SOUT2;
		   rSOUT3 = SOUT3;
		   pST = 1;
		   state = 5;
		end
		5: begin
		   state = 6;
		end
		6: begin
		   pST = 0;
		   rIN1 = rSOUT1;
		   rIN2 = rSOUT2;
		   rIN3 = rSOUT3;
		   if (pRD == 1 & pRES == 0) state = 7;
		   if (pRD == 1 & pRES > 0) state = 1;
		end
		7: begin
		   RD = 1;
		   RES = rSOUT1;
		   rIN1 = IN1;
		   rIN2 = IN2;
		   rIN3 = IN3;
		   if (ST == 1) state = 1;
		   
		end
	  endcase // case (state)
	  
   end

   mock mod1(RST, ST1, CLK, RD1, SOUT1, rIN1, rIN2, rIN3);
   mock mod2(RST, ST2, CLK, RD2, SOUT2, rIN1, rIN2, rIN3);
   mock mod3(RST, ST3, CLK, RD3, SOUT3, rIN1, rIN2, rIN3);
   mock pred(RST, pST, CLK, pRD, pRES, rIN1, rIN2, rIN3);

endmodule // modulename

   