`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
module gpio(

input wire [15:0] shift,
input wire [15:0] DDR,
input wire DDR_enable,
input wire PORT_enable,
output reg [15:0] pin_data,
input clk,
input reset,
inout wire [15:0] pins

);

reg[15:0] PORTX;
reg[15:0] DDRX;

always@(posedge clk or posedge reset)begin
if(reset) begin
DDRX<=4'h0000;
PORTX<=4'h0000;

end else begin
if(DDR_enable) DDRX<=DDR;
if(PORT_enable) PORTX<=shift;
end
end

assign pins[0]=((DDRX[0]) ? PORTX[0] : 1'bz);
assign pins[1]=((DDRX[1]) ? PORTX[1] : 1'bz);
assign pins[2]=((DDRX[2]) ? PORTX[2] : 1'bz);
assign pins[3]=((DDRX[3]) ? PORTX[3] : 1'bz);
assign pins[4]=((DDRX[4]) ? PORTX[4] : 1'bz);
assign pins[5]=((DDRX[5]) ? PORTX[5] : 1'bz);
assign pins[6]=((DDRX[6]) ? PORTX[6] : 1'bz);
assign pins[7]=((DDRX[7]) ? PORTX[7] : 1'bz);
assign pins[8]=((DDRX[8]) ? PORTX[8] : 1'bz);
assign pins[9]=((DDRX[9]) ? PORTX[9] : 1'bz);
assign pins[10]=((DDRX[10]) ? PORTX[10] : 1'bz);
assign pins[11]=((DDRX[11]) ? PORTX[11] : 1'bz);
assign pins[12]=((DDRX[12]) ? PORTX[12] : 1'bz);
assign pins[13]=((DDRX[13]) ? PORTX[13] : 1'bz);
assign pins[14]=((DDRX[14]) ? PORTX[14] : 1'bz);
assign pins[15]=((DDRX[15]) ? PORTX[15] : 1'bz);

always@(posedge clk or posedge reset)begin
if(reset) begin
pin_data<=4'h0000;
end else begin
pin_data<=pins;
end
end

endmodule


