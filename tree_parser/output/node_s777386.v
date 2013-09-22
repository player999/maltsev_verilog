module  node_s777386(RST, ST, CLK, RD, RES, IN);
	input wire RST;
	input wire ST;
	input wire CLK;
	output reg RD;
	output reg [15:0] RES;
	input wire [15:0] IN;
	reg STold;
	reg RF;

	always @(posedge CLK) begin
		if(RST == 1) begin
			RD = 1;
			RF = 1;
		end else begin
			if(RF == 1) begin
				RD = 1;
			end
			if(RF == 0) begin
				RES = IN + 1;
				RF = 1;
			end
			if(ST == 1 && STold == 0) begin
                                RF = 0;
				RD = 0;
                        end
		end
		STold = ST;
	end	
endmodule
