
module memory_instruction(
input clk,
input reset,
input write_enable,
input wire [11:0] address,
input wire[31:0] ins_in,
output reg[31:0] ins_out


    );
    reg [11:0] address_in;
    reg [31:0] instruction [0:4095];
    always@(posedge clk)begin
    if (reset)begin
    address_in<=12'b0;
        ins_out<=instruction[12'b0];
    end else begin
    
    if(~write_enable)begin
    if(address_in<4096)begin
    instruction[address_in]<=ins_in;
    address_in<=address_in+1'b1;
    end else begin
    address_in<=12'b0;
    end
    
    end
    ins_out<=instruction[address];
    end
    end
endmodule
// 
//////////////////////////////////////////////////////////////////////////////////


