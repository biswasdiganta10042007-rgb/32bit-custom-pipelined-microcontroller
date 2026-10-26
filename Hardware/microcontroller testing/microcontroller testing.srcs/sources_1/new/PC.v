`timescale 1ns / 1ps

module PC(
input clk,
input reset,
input halt,
input jump,
input wire[11:0] jump_address,
output wire[11:0] ADDRESS_OUT

    );
    reg [11:0] address_out;
    always@(posedge clk or posedge reset)begin
    if(reset)begin
    address_out<=12'b0;
    end else
     if(halt) begin
    address_out<=address_out;
    end else 
    if(jump==1'b0) begin
    address_out<=jump_address;
    end else begin
    address_out<=address_out+1'b1;
    end
    
    end
    assign ADDRESS_OUT=address_out;
endmodule
