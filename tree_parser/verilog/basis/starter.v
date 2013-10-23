module starter(RST, CLK, Stin, Stout);
   parameter pulse_length = 3;
   input wire RST;
   input wire Stin;
   input wire CLK;
   output reg Stout;
   reg 		  Stold;
   reg [1:0]  CNT;
   
   always @(posedge CLK)
	 begin
		if (RST == 1)
		  begin
			 CNT = 0;
			 Stout = 0;
		  end
		
		if(CNT > 0)
		  begin
			 CNT = CNT - 1;
			 if(CNT == 0)
			   begin
				  Stout = 0;
			   end			 
		  end
		if((Stin == 1) && (Stold == 0))
		  begin
			 CNT = pulse_length;
			 Stout = 1;			 
		  end
		Stold = Stin;
	 end // always @ (posedge CLK)
   endmodule