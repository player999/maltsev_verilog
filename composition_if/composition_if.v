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
   input wire          RST;
   input wire          ST;
   input wire          CLK;
   output reg          RD;
   output reg [16-1:0] RES;
   input wire [16-1:0] IN1;
   input wire [16-1:0] IN2;
   input wire [16-1:0] IN3;
   reg [3:0] 		   state;
   wire [16-1:0] 	   SOUT_YES;
   wire [16-1:0] 	   SOUT_NO;
   wire [16-1:0] 	   pRES;
   wire [16-1:0] 	   lRES; 	   
   wire 			   yRD;
   wire 			   nRD;
   wire 			   pRD;
   wire 			   lRD;
   reg 				   yST;
   reg 				   nST;
   reg  			   pST;

   assign lRD = nRD & yRD & pRD;
   assign lRES = pRES > 0?SOUT_YES:SOUT_NO;
   mock_yes yes(RST, yST, CLK, yRD, SOUT_YES, IN1, IN2, IN3);
   mock_no no(RST, nST, CLK, nRD, SOUT_NO, IN1, IN2, IN3);
   mock_pred pred(RST, pST, CLK, pRD, pRES, IN1, IN2, IN3);

   always @(posedge CLK) begin
	  if (RST == 1) begin
		 yST = 0;
		 nST = 0;
		 pST = 0;
		 state = 0;
		 RD = 1;
		 RES = 0;		
	  end
	  case (state)
		0:begin
		   RD = 1;
		   if (ST == 1) state = 1;
		end
		1:begin
		   yST = 1;
		   nST = 1;
		   pST = 1;
		   RD = 0;
		   state = 2;
		end
		2:begin
		   state = 3;
		end
		3:begin
		   yST = 0;
		   nST = 0;
		   pST = 0;
		   if (lRD == 1) state = 4;		   
		end
		4:begin
		   RD = 1;
		   RES = lRES;
		   state = 5;
		end
		5:begin
		   RD = 1;
		   if(ST == 1) state = 1;
		end
	  endcase // case (state)
   end // always @ (posedge CLK)
endmodule // modulename
	 