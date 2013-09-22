module root_tb();
    wire RST;
    wire ST;
    wire CLK;
    wire RD;
    wire [15:0] RES;
    reg rRST;
    reg rST;
    reg rCLK;
	wire [15:0] IN0;
	wire [15:0] IN1;
	wire [15:0] IN2;
	wire [15:0] IN3;
	wire [15:0] IN4;
	reg [15:0] rIN0;
	reg [15:0] rIN1;
	reg [15:0] rIN2;
	reg [15:0] rIN3;
	reg [15:0] rIN4;
    
    root_R839304 root(RST, ST, CLK, RD, RES, IN0, IN1, IN2, IN3, IN4);

	assign IN0 = rIN0;
	assign IN1 = rIN1;
	assign IN2 = rIN2;
	assign IN3 = rIN3;
	assign IN4 = rIN4;
    assign CLK = rCLK;
    assign RST = rRST;
    assign ST = rST;

    initial begin
        $dumpfile("/home/player999/Work/disseratation/maltsev_verilog_NW/tree_parser/output/dump.vcd");
        $dumpvars;
        rCLK = 0;
        rRST = 1;
        rST = 0;
	rIN0 = 2;
	rIN1 = 3;
	rIN2 = 3;
	rIN3 = 2;
	rIN4 = 3;
        #15 rRST = 0;
        #20 rST = 1;
        #10 rST = 0;
        #100000 $finish;
    end

    always #5 rCLK = !rCLK;

endmodule
