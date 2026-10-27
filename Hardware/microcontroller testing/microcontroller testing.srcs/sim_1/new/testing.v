`timescale 1ns / 1ps

module tb_top_assembly;

    // ---------------------------------------------------------
    // Top-Level Interface Signals
    // ---------------------------------------------------------
    reg clk;
    reg reset;
    reg write_ins_enable;
    reg write_data_enable;
    reg [31:0] instruction_data;
    reg [31:0] memory_data;

    // ---------------------------------------------------------
    // Device Under Test (DUT) Instantiation
    // ---------------------------------------------------------
    top_assembly uut (
        .clk(clk),
        .reset(reset),
        .write_ins_enable(write_ins_enable),
        .write_data_enable(write_data_enable),
        .instruction_data(instruction_data),
        .memory_data(memory_data)
    );

    // ---------------------------------------------------------
    // Clock Generation (50 MHz / 20ns period)
    // ---------------------------------------------------------
    always begin
        #10 clk = ~clk;
    end

    // ---------------------------------------------------------
    // Stimulus & File Forcing Initialization
    // ---------------------------------------------------------
    initial begin
        // 1. Set explicit initial values AT time zero
        clk = 0;
        reset = 1;             // START AT 1: Force system into a known reset state immediately
        write_ins_enable = 1;  // Disable active-low sequential load hardware loop
        write_data_enable = 1; // Disable active-low sequential load hardware loop
        instruction_data = 32'h0;
        memory_data = 32'h0;

        // 2. Load memory arrays directly from your local .mem assets
        $readmemh ("instructions.mem", uut.I.instruction);
        $readmemb("data.mem", uut.D.memory);

        // 3. Hold the reset state high for 4 full clock cycles (80ns) 
        // This ensures the pipelined control unit wipes out all random startup data!
        #80;
        
        // 4. Drop reset to 0 to start normal processor execution
        reset = 0;
        
        // 5. Let the simulation run for a safe window
        #1000;
         $writememh("updated_data.mem", uut.D.memory);

        
        $finish;
    end
    
    
    // ---------------------------------------------------------
    // Waveform Trace Debug Monitor
    // ---------------------------------------------------------
 initial begin
        $monitor("Time=%0dns | PC_Addr=%d | Raw_Ins=%h | Opcode=%h | fetch=|", 
                 $time, uut.ADDRESS, uut.INSTRUCTION, uut.opcode, uut.data_val, uut.data_val);
    end
endmodule
