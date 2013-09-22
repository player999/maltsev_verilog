module posedge_reg(RST, CLK, RESin, RESout);
   input wire RST;
   input wire CLK;
   input wire RESin;
   output reg RESout;
   reg 		  RESold;
   
   
   always @(posedge CLK)
	 begin
		if(RST == 0)
		  begin
			 RESout = 1;
			 RESold = 1;
		  end
		else
		  begin
			 if((RESold == 0) && (RESin == 1))
			   begin
				  RESout = 1;
			   end
		  end
		if (RESin == 0)
		  begin
			 RESold = 0;
			 RESout = 0;
		  end
		else
		  begin
			 RESold = 1;
		  end
	 end
endmodule