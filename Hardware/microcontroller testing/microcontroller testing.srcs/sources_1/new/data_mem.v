`timescale 1ns / 1ps
module memory_data(
input clk,
input rst,
input write_enable,
input write_cu,
input wire[7:0] address_reg_a,
input wire[7:0] address_reg_b,
input wire[7:0] address_reg_out,
input wire[31:0] data_in,
input wire[31:0] data_in_processed,
output reg[31:0] data_out_a,
output reg[31:0] data_out_b


    );
    
    reg [7:0] address_in;
 reg [31:0] memory [0:255];
 always@(posedge clk)begin
 if(rst)begin
 address_in<=8'h00;
 end else 

 if(~write_enable)begin
 if(address_in<255)begin
 memory[address_in]<=data_in;
 address_in<=address_in+1'b1;
 end
 if (write_cu) begin
                memory[address_reg_out] <= data_in_processed;
            end
 end
 end
 
 always@(*)begin
 data_out_a=memory[address_reg_a];
 data_out_b=memory[address_reg_b];
 end
 
 
 
endmodule


