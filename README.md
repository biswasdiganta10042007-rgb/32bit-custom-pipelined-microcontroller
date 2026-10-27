# 32-Bit Custom Pipelined Single Core Microcontroller & Nested Software Toolchain

A vertically integrated computing ecosystem featuring a custom-designed **32-bit pipelined processor architecture** implemented in Verilog (AMD Xilinx Vivado) and a robust **compiler/assembler toolchain** implemented in Python (NumPy). 

The ecosystem compiles a custom high-level programming language down to optimized hardware instructions, featuring **dynamic structural data-forwarding**, support for **arbitrary conditional nesting (`if`/`while`)**, fixed-point fractional scaling, and direct memory-mapped **GPIO peripheral matrices**.

---

## 📁 Repository Structure

*   `/hardware` - Vivado project files (`.xpr`), structural source codes (`.srcs`), and board constraints.
*   `/compiler` - Object-oriented stack-based compiler (`CustomCompiler`) translating high-level code with control loops into intermediate assembly blocks.
*   `/assembler` - Micro-assembler mapping human-readable instruction mnemonics to physical 32-bit hex-encoded binaries (`.mem`).
*   `/examples` - High-level test applications (`program.txt`), dry run simulation traces, and testbenches.

---

## 🛠️ Hardware Specification & Microarchitecture

*   **Data Word Length:** 32-bit Data Paths.
*   **Addressing Space:** 12-bit Instruction Address Bus (up to 4096 addressable execution blocks).
*   **Data Register Bank:** 256 internal general-purpose registers (`R0` through `R255`).
    *   *Note: `R0` is structurally tied to the `cond` register output for evaluation routines.*
*   **Pipeline Stage Optimization:** Structural Fetch & Decode boundaries.
*   **Data Hazard Mitigation:** Integrated structural **Data-Forwarding Logic (`k` and `l` bypass tracking)**. The `control_unit_pipelined` automatically checks if the current execution's target destination matches subsequent source inputs. If matched, it forces the ALU to read inputs instantly from raw processor loop feedback lines, wiping out structural read-after-write (RAW) data hazards.
*   **Peripherals:** Fully programmable Integrated 16-bit wide GPIO Controller featuring tri-state high-impedance (`1'bz`) safety structures driven by `DDRX` (Data Direction) and `PORTX` registers.

---

## 📑 Instruction Set Architecture (ISA) & Bit-Mapping

Every runtime machine action is packed tightly into a solid **32-bit layout**:

| Bits [31:28] | Bits [27:24] | Bits [23:16] | Bits [15:8] | Bits [7:0] | Bits [11:0] |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OPCODE** (Mux Select) | **ALU SELECT** | **Operand Register 1** | **Result / Destination** | **Operand Register 2** | **JUMP ADDRESS** (Conditional Space) |

### 1. Control Opcodes (`OPCODE` Mux Settings)
*   `4'b0000` : **NOP / Bubble** (Sequential incrementation marker)
*   `4'b0110` : **ALU_EN** (Enables arithmetic/logic calculation execution paths)
*   `4'b0111` : **HLT** (Suspends execution loops and freezes the Program Counter)
*   `4'b1100` : **JUMP** (Triggers immediate or conditional Branch Vectors)
*   `4'b1111` : **WRITE** (Enables processor execution write-backs to memory)
*   `4'b1101` : **GPIO Config** (Activates peripheral control signals)
*   `4'b1110` : **PIN Read** (Toggles external reading frames)

### 2. Operational Opcodes (`ALU SELECT` Settings)
*   `4'b0101` : **ADD** | `4'b0110` : **SUB** | `4'b0111` : **MUL**
*   `4'b0000` : **AND** | `4'b0001` : **OR**  | `4'b0010` : **XOR**
*   `4'b1101` : **NOT_A** | `4'b1110` : **NOT_B**
*   `4'b1100` : **SHIFT_BITS** | `4'b1011` : **SHIFT_0** | `4'b1010` : **SHIFT_1**
*   `4'b0100` : **EQUAL** | `4'b1001` : **GREATER** | `4'b1000` : **LESS**

---

## 💻 Software Toolchain Mechanics

### 1. The Custom Stack-Based Compiler (`compiler.py`)
Parses custom high-level files (`program.txt`), allocates local variable addresses across an internal `data_array`, and generates structured data blocks.
*   **Variable Allocation & Typing:** Handles `int` allocations natively. For `float` calculations, it implements a fixed-point fractional layout scaling values by **\(2^7\) (`int(data * (2 ** 7))`)** to preserve computational precision across raw 32-bit registers.
*   **Control Flow Stacking & Infinite Nesting:** Uses an object-oriented block stack mechanism. When an `if` or `while` block is encountered, the state is pushed onto the stack. Jumps are dynamically updated once `endif` or `endwhile` tokens match, enabling multi-level deep control loop structures.
*   **Pipeline Flash Injection:** Because the processor relies on predictive fetch paths, the compiler systematically appends **exactly two `NOP 0 0 0 0` pipeline bubbles** directly following every compiled branch instruction to clear out pipeline trace execution hazards.

### 2. The Binary Assembler (`assembler.py`)
Tokenizes intermediate code inputs, shifts bit segments into place, and scales register references by a strict **\(-1\) offset** (`int(val)-1`) so that code-level `R1` points natively to address space `8'h00`. Outputs an optimized 8-character hardware Hex string (`08X`).

---

## 🚀 Execution Workflow Guide

To execute software applications directly on your physical hardware modules, follow this step-by-step layout chain:

### Step 1: Write Your High-Level Source Code
Create a source file at `examples/program.txt`. Example syntax:
```text
int alpha = 10
int beta = 20
int result = 0
while alpha < beta
    result = alpha + beta
endwhile
```
# RULES to be Followed
* important point: space should be there after every variable number and operator
* Example: int a=30 or b=c+d would not work 
* the correct way is : int a = 30 or b = c + d
* the first first line should be a dummy variable like ( int dummy = 0 ) and the use od that variable should be avoided as the internal processor needs a dummy variable for reset and halt.
# LIMITATIONS
1. Every variable used must be initialized to some value before use and direct use of numbers(integers and floating point numerals cannot be done).
2. Floating point numerals which will be used as operands must be of only two decimals places or less and has to be less than (511.99)
any integer used as an operand must be less than (2^16)-1 as this is the maximum size of operator that can be used.
3. If any floating point literal has more than two digits after decimal point those will be truncated

### Step 2: Compile the High-Level Project
Run the compiler engine to allocate variable matrices into `data.mem` and output raw structured code lines into `ASSEMBLY_code.txt`:
```bash
python compiler/compiler.py
```

### Step 3: Assemble the Binaries
Run the assembler script to translate your assembly outputs into clean 32-bit hexadecimal words inside `instructions.mem`:
```bash
python assembler/assembler.py
```

### Step 4: Run Hardware Simulation Testbenches
1. Open **AMD Xilinx Vivado** and load the hardware wrapper project file `/hardware/top_assembly.xpr`.
2. Map the simulation runtime properties to load `instructions.mem` directly into your `memory_instruction` model array block.
3. Map the variable file `data.mem` directly into your `memory_data` model bank layout block.
4. Execute **Run Behavioral Simulation**. Trace waves to view live ALU changes, pipeline data-forwarding triggers, and pin state alterations!
5. An example test bench is provided in the main .xpr file . the same syntax can be used to run tests on the microcontroller with program and data files changed accordingly.
