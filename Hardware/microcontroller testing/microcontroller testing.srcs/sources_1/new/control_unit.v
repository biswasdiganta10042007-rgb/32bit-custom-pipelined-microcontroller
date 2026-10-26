`timescale 1ns / 1ps


module control_unit_pipelined(
input clk,
input halt,
input rst,


input wire[11:0] ins_no,
output reg[11:0] ins_address,
input wire[31:0] instructions,
output wire[3:0] control_mux_out,
output wire[3:0] alu_select,
output wire [7:0] operand_1_add,
output wire [7:0] operand_2_add,
output wire [7:0] result_add,
input wire write_memory,
input wire[31:0] calc_data,
output reg write_cu,
output wire[11:0] instruction_address_out,
output reg[31:0] data_out,
output reg l,
output reg k
);
reg [31:0] fetch;

always@(posedge clk)begin
 if(~halt) begin
 ins_address<=ins_no;
 fetch<=instructions;
 end
end
 
reg [3:0] op_code;
reg [3:0] select;
reg [7:0] operand_1;
reg [7:0] operand_2;
reg [7:0] data_out_address;
reg [11:0] jump_address;
always@(posedge clk)begin
 if (rst) begin
            op_code          <= 4'b0;
            select           <= 4'b0;
            operand_1        <= 8'b0;
            operand_2        <= 8'b0;
            data_out_address <= 8'b0;
            jump_address     <= 12'b0;
            k<=1'b0;
            l<=1'b0;
        end else 
        if (~halt) begin
 op_code<={fetch[31:28]};
 select<={fetch[27:24]};
 operand_1<={fetch[23:16]};
 data_out_address<={fetch[15:8]};
 operand_2<={fetch[7:0]};
 jump_address<={fetch[11:0]};
 
 if({fetch[15:8]}=={instructions[7:0]})begin
 k<=1'b1;
 end
 else begin
 k<=1'b0;
 end
 if({fetch[15:8]}=={instructions[23:16]})begin
 l<=1'b1;
 end else begin 
  l<=1'b0;
 end
 end
end 

 

assign control_mux_out=op_code;
assign instruction_address_out=jump_address;
assign result_add=data_out_address;
assign operand_1_add=operand_1;
assign operand_2_add=operand_2;
assign alu_select=select;

reg [31:0] write_to_mem;


always@(posedge clk)begin
if (rst) begin
     write_to_mem <= 32'b0;
     write_cu     <= 1'b0;
end else if (~halt) begin
write_to_mem<=calc_data;
if(write_memory)begin
write_cu<=1'b1;
end else begin
write_cu<=1'b0;
end
data_out<=write_to_mem;
end
end

endmodule