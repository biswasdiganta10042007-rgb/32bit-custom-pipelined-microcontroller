ALUCODES = {
    "ADD": "0101", "SUB": "0110", "MUL": "0111", "AND": "0000",
    "OR": "0001", "XOR": "0010", "NOT_A": "1101", "NOT_B": "1110",
    "SHIFT_BITS": "1100", "SHIFT_0": "1011", "SHIFT_1": "1010",
    "EQUAL": "0100", "GREATER": "1001", "LESS": "1000"
}

OPCODES = {
    "NOP": "0000", "ALU_EN": "0110", "HLT": "0111", "JUMP": "1100", "WRITE": "1111"
}


def assemble_code(instruction_text):
    tokens = instruction_text.replace(",", " ").split()
    if not tokens:
        return None

    opcode = tokens[0]
    if opcode not in OPCODES:
        print(f"Error: Unknown opcode '{opcode}'")
        return None

    op = OPCODES[opcode]


    if op == "1100":

        address_val = int(tokens[1])
        address_bin = format(address_val, "012b")
        
        ins_bin = address_bin + "0000000000000000" + op

        hex_ins = format(int(ins_bin, 2), "08X")
        print(f"Assembly Instruction: {instruction_text}")
        print(f"32 bit Instruction (HEX): {hex_ins}")
        return hex_ins


    elif op == "0000":

        ins_bin = "00000000000000000000000000000000"
        hex_ins = format(int(ins_bin, 2), "08X")
        print(f"Assembly Instruction: {instruction_text}")
        print(f"32 bit Instruction (HEX): {hex_ins}")
        return hex_ins


    else:

        alucode = tokens[1]
        in1 = tokens[2]
        in2 = tokens[3]
        out = tokens[4]

        val1 = in1.replace("R", "")
        val2 = in2.replace("R", "")
        res = out.replace("R", "")

        alu = ALUCODES[alucode]
        bin_val1 = format((int(val1)-1), "08b")
        bin_val2 = format((int(val2)-1), "08b")
        bin_res = format((int(res)-1), "08b")


        ins_bin = op + alu + bin_val1 + bin_res + bin_val2
        print(ins_bin)
        hex_ins = format(int(ins_bin, 2), "08X")

        print(f"Assembly Instruction: {instruction_text}")
        print(f"Blocks: [ALU:{alu}, OP:{op}, R_In1:{bin_val1}, R_In2:{bin_val2}, HEX:{hex_ins}]")
        print(f"32 bit Instruction (HEX): {hex_ins}")
        return hex_ins



input_path = r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\ASSEMBLY_code.txt"
output_path = r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\instructions.mem"

with open(input_path, "r") as infile, open(output_path, "w") as outfile:
    for line in infile:
        cleaned_line = line.strip()
        if not cleaned_line or "Error" in cleaned_line:
            continue
        progdata = assemble_code(cleaned_line)
        if progdata is not None:
            outfile.write(progdata + "\n")
