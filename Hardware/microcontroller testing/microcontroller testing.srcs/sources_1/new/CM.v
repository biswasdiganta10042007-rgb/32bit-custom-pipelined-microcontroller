`timescale 1ns / 1ps

 
module control_mux(
 input wire [3:0] mux_select,
 
 
 output reg JUMP,
 output reg WRITE,
 output reg HLT,
 output reg alu_enable,
 output reg ddr_enable,
 output reg port_enable,
 output reg pin_enable,
 
 input cond
 );
 
 
 
 always@(*)begin
 
 
 
 HLT=1'b0;
 JUMP=1'b1;
 WRITE=1'b0;
 alu_enable=1'b0;
 ddr_enable=1'b0;
 port_enable=1'b0;
 pin_enable=1'b0;
  
 case(mux_select)
 4'b0000:begin
 JUMP=1'b1;
 end

 4'b0110:begin
 alu_enable=1'b1;
 end
 4'b0111:begin
 HLT=1'b1;
 end
 4'b1100:begin
 if(cond==1'b1)begin
 JUMP=1'b1;
 end else begin 
 JUMP=1'b0;
 end
 end
 4'b1111:begin
 WRITE=1'b1;
 end
 4'b1101:begin
 ddr_enable=1'b1;
 port_enable=1'b1;
 end
 4'b1110:begin
 pin_enable=1'b1;
 end
 default:begin
 JUMP=1'b1;
 end
 endcase
 
 
 end
 endmodule