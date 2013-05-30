module operation_i_bw16_inc3_si2(RST, ST, CLK, RD, RES, IN0, IN1, IN2);
	input wire RST;
	input wire ST;
	input wire CLK;
	output reg RD;
	output reg [16-1:0] RES;
	reg STold;
	reg RF;
	input wire [15:0] IN0;
	input wire [15:0] IN1;
	input wire [15:0] IN2;


	always @(posedge CLK) begin
		if(RST == 1) begin
			RD = 1;
			RF = 1;
		end else begin
			if(RF == 1) begin 
				RD = 1;
			end
			if(RF == 0) begin
				RES = IN2;
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
