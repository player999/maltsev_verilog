module rdbuf(RST, CLK, RDin, RD);
	input RST, CLK, RDin;
	output reg RD;
	reg buf0, buf1, buf2;
	always @(posedge CLK) begin
		if(RST == 1) begin
			buf0 = 0;
			buf1 = 0;
			buf2 = 0;
		end else begin
			if(buf0 == 1 && buf1 == 1 && RDin == 1) begin
				RD = 1;
			end else begin
				RD = 0;
			end
			if (RDin == 0) begin
				RD = 0;
			end
		end
		buf2 = buf1;
		buf1 = buf0;
		buf0 = RDin;
	end
endmodule