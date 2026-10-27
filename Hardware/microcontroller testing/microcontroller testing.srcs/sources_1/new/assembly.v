`timescale 1ns / 1ps

 
module top_assembly(
input clk,
input reset,
input write_ins_enable,
input write_data_enable,
input wire[31:0] instruction_data,
input wire[31:0] memory_data

    );
    
    
    wire [31:0] INSTRUCTION;
    wire [11:0] ADDRESS;
    wire [11:0] INS;
    memory_instruction I(
    .clk(clk),
    .reset(reset),
    .ins_in(instruction_data),
    .write_enable(write_ins_enable),
    .ins_out(INSTRUCTION),
    .address(INS)
    );
     
    wire halt;
    wire jump;
    wire [11:0] jump_ADDRESS;
    
    
    PC p(
    .clk(clk),
    .reset(reset),
    .halt(halt),
    .jump(jump),
    .jump_address(jump_ADDRESS),
    .ADDRESS_OUT(ADDRESS)
    );
    
    wire [7:0] opp_1;
    wire [7:0] opp_2;
    wire [7:0] opp_res;
    wire CU;
    wire [31:0] data_A;
    wire [31:0] data_B; 
    wire [31:0] data_val;
    wire [31:0] mem_data;
    wire write;
    
     memory_data D(
     .clk(clk),
     .rst(reset),
     .write_enable(write_data_enable),
     .write_cu(CU),
     .address_reg_a(opp_1),
     .address_reg_b(opp_2),
     .address_reg_out(opp_res),
     .data_in(memory_data),
     .data_in_processed(mem_data),
     .data_out_a(data_A),
     .data_out_b(data_B)
     
     );
   
    wire [4:0] opcode;
    wire [4:0] alu_sel;
    wire a;
    wire b;
    wire [31:0] feedback;
   control_unit_pipelined MAIN_C(
   .clk(clk),
   .k(a),
   .l(b),
   .halt(halt),
   .rst(reset),
   .ins_no(ADDRESS),
   .ins_address(INS),
   .instructions(INSTRUCTION),
   .control_mux_out(opcode),
   .alu_select(alu_sel),
   .operand_1_add(opp_1),
   .operand_2_add(opp_2),
   .result_add(opp_res),
   .write_memory(write),
   .calc_data(data_val),
   .write_cu(CU),
   .feedback(feedback),
   .instruction_address_out(jump_ADDRESS),
   .data_out(mem_data)
   );
   
   wire alu_EN;
   wire cond;
   wire ddr_en;
   wire port_en;
   wire [15:0] shift_res;
   wire [15:0] pin_value;
   wire [15:0] DDR;
   
   alu A(
   .val_in1(data_A),
   .val_in2(data_B),
   .shift(data_A[15:0]),
   .sel(alu_sel),
   .k(a),
   .l(b),
   .feedback_data(feedback),
   .shift_count(data_B),
   .shift_index(data_B),
   .alu_enable(alu_EN),
   .val_out(data_val),
   .shift_out(shift_res),
   .cond(cond),
   .data_dir(data_B[15:0]),
   .pin_data(pin_value),
   .DDR(DDR)
   );
    
    control_mux CM(
    .mux_select(opcode),
    .JUMP(jump),
    .HLT(halt),
    .WRITE(write),
    .cond(cond),
    .alu_enable(alu_EN),
    .ddr_enable(ddr_en),
    .pin_enable(port_en)
    );
    
    
    
    gpio G(
    .clk(clk),
    .reset(reset),
    .shift(shift_res),
    .DDR(DDR),
    .DDR_enable(ddr_en),
    .PORT_enable(port_en),
    .pin_data(pin_value),
    .pins()
    );
    
    
    
    
    
endmodule
