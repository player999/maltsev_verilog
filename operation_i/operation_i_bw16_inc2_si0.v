module operation_i_bw16_inc2_si0(RST, ST, CLK, RD, RES, IN0, IN1);
	input wire RST;
	input wire ST;
	input wire CLK;
	output reg RD;
	output reg [16-1:0] RES;
	reg STold;
	reg RF;
	input wire [15:0] IN0;
	input wire [15:0] IN1;


	always @(posedge CLK) begin
		if(RST == 1) begin
			RD = 1;
		end else begin
			if(RF == 1) begin
				RD = 1;
			end
			if(RF == 0) begin
				RES = IN0;
				RF = 1;
			end
			if(ST == 1 && STold == 0) begin
                                RD = 0;
				RF = 0;
                        end
		end
		if(ST == 1) begin
			STold = 1;
		end else begin
			STold = 0;
		end
	end	
endmodule
