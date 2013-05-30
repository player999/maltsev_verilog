module operation_s_16(RST, ST, CLK, RD, RES, IN);
	input wire RST;
	input wire ST;
	input wire CLK;
	output reg RD;
	output reg [16-1:0] RES;
	input wire [16-1:0] IN;
	reg STold;
	always @(posedge CLK) begin
		if(RST == 1) begin
			RD = 1;
		end else begin
			if(RD == 0) begin
				RES = IN + 1;
				RD = 1;
			end
			if(ST == 1 && STold == 0) begin
                                RD = 0;
                        end
		end
		STold = ST;
	end	
endmodule
