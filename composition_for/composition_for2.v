module %NAME%(
					   RST,
					   ST,
					   CLK,
					   RD,
					   RES,
					   //%IN_LIST%,
			           IN1,
			           IN2,
			           IN3
);
   input wire          RST;
   input wire          ST;
   input wire          CLK;
   output reg          RD;
   output reg [16-1:0] RES;

//Module inputs
//%IN_DEF%
   input wire [16-1:0] IN1;
   input wire [16-1:0] IN2;
   input wire [16-1:0] IN3;

//Local outputs
//%SOUT_DEF%
   wire [16-1:0] 	   SOUT1;
   wire [16-1:0] 	   SOUT2;
   wire [16-1:0] 	   SOUT3;
   
//%rSOUT_DEF%
   wire [16-1:0] 	   rSOUT1;
   wire [16-1:0] 	   rSOUT2;
   wire [16-1:0] 	   rSOUT3;

//Local inputs
//%SIN_DEF%
   reg [16-1:0] 	   SIN1;
   reg [16-1:0] 	   SIN2;
   reg [16-1:0] 	   SIN3;

//Local modules ready signals
//%RD_DEF%
   wire 			   RD1;
   wire 			   RD2;
   wire 			   RD3;
   
//%RD_DEF_OLD%
  
//Local modules start signals
   
   wire 			   RD_LOCAL;
   wire 			   RD_PREDIC;
   reg 				   ST_OLD1;
   reg 				   ST_OLD2;
   reg 				   STI;
   wire 			   ST_PREDIC;
   wire [16-1:0]	   RES_PREDIC;
   
//%ASSGIN_RD%
   assign RD_LOCAL = RD1 & RD2 & RD3;
   assign ST_PREDIC = RD_LOCAL;
   
   always @(posedge CLK) begin
	  if (RST == 1) begin
		 RD = 1;
		 RES = 0;
//%SIN_CLR%
		 SIN1 = 0;
		 SIN2 = 0;
		 SIN3 = 0;
//%ST_CLR%
		 ST1 = 0;
		 ST2 = 0;
		 ST3 = 0;
//%CLR_SOUT%
		 rSOUT1 = 0;
		 rSOUT2 = 0;
		 rSOUT3 = 0;
		 ST_OLD1 = 0;
		 ST_OLD2 = 0;
		 
	  end else begin
		 if (RD == 0) begin
			if (ST_OLD1 == 1 && ST_OLD2 == 1) begin
			   RD = 0;
			   if (RD_LOCAL > 0) begin
				  rSOUT1 = SOUT1;
				  rSOUT2 = SOUT2;
				  rSOUT3 = SOUT3;
				  ST1 = 1;
				  ST2 = 1;
				  ST3 = 1;
				  ST_PREDIC = 1;
			   end
			   if (RD_PREDIC == 1) begin
				  
			   end
			end
		 end		 	 
	  end
	  
   end

								
//%MODULES_DEF%
   one mod1(RST,STI,CLK,RD1,SOUT1,IN1,IN2,IN3);
   two mod2(RST,STI,CLK,RD2,SOUT2,IN1,IN2,IN3);
   tre mod3(RST,STI,CLK,RD3,SOUT3,IN1,IN2,IN3);
   
//predicate %PREDIC_NAME%(%IN_LIST%)
   prd pre(RST,ST_PREDIC,CLK,RD_PREDIC,RES_PREDIC,IN1,IN2,IN3);