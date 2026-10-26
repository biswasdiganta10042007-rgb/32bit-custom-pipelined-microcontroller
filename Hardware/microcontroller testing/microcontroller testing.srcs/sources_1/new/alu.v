`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
module alu(
input k,
input l,
input [31:0] val_in1,
input [31:0] val_in2,
input [3:0] sel,
input [31:0] feedback_data,
input [15:0] shift,
input [15:0] data_dir,
output [15:0] DDR,
input [3:0] shift_count,
input [3:0]shift_index,
input alu_enable,
output reg[31:0] val_out,
output reg[15:0] shift_out,
input [15:0] pin_data,
output reg cond
);
wire[3:0] select;
assign select=(alu_enable)? sel:4'b1111;
wire [15:0] in_1;
wire [15:0] in_2;
reg [15:0] shift_in;
    assign in_1 = (l) ? feedback_data : val_in1;
    assign in_2 = (k) ? feedback_data : val_in2;


always@(*)begin

  val_out =32'b0;
  shift_out=16'b0;
  
  cond=1'b0;

shift_in=shift;

case(select)
4'b0000: begin
        val_out=(in_1&in_2);
        end
4'b0001:begin 
        val_out=(in_1 | in_2);
        end
4'b0010:begin 
        val_out=in_1^in_2;
        end
4'b0100:begin
       if(in_1==in_2)begin
       cond=1'b1;
       end else begin 
       cond=1'b0;
       end
        end
4'b0101:begin
        val_out=in_1+in_2;
        end
4'b0110:begin
        val_out=in_1-in_2;
        end
4'b0111:begin
        val_out=in_1*in_2;
        end
4'b1000:begin
         if(in_1<in_2)begin
         cond=1'b1;
         end 
         end
4'b1001:begin
        if(in_1>in_2)begin
         cond=1'b1;
         end 
         end
4'b1010:begin
        shift_out=shift_out | (1'b1<<shift_index);
        end
4'b1011:begin
        shift_out=shift_out & ~(1'b1<<shift_index);
        end
4'b1100:begin                 
        shift_out=shift_in<<shift_count;
        end 
4'b1101:begin                 
        val_out=~in_1;
        end
4'b1110:begin                 
        val_out=~in_2;
        end        
 4'b0011:begin
         val_out=pin_data^data_dir;
         end       
default:begin
        val_out=val_out;
        shift_out=shift_out;
        end
        endcase
 end 
   assign DDR=data_dir;      

endmodule
