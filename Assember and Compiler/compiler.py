import numpy as np


class CustomCompiler:
    def __init__(self):
        self.my_structure = np.dtype([
            ('variable', 'U10'),
            ('value', 'i4'),
            ('address', 'i4')
        ])
        self.data_array = np.zeros(255, dtype=self.my_structure)
        self.data_array[0] = ('ZZ', 0, 0)
        self.active_data_index = 1
        self.program_counter = 0
        self.OPERATORS = {
            "+": "ALU_EN ADD", "-": "ALU_EN SUB", "*": "ALU_EN MUL",
            "&": "ALU_EN AND", "^": "ALU_EN XOR", "|": "ALU_EN OR ",
            ">": "ALU_EN GREATER", "<": "ALU_EN LESS", "==": "ALU_EN EQUAL"
        }

    def data_assign(self, line):
        tokens = line.split()
        data_type = tokens[0]
        variable = tokens[1]
        data = tokens[3]
        wd1 = "int"
        wd2 = "float"

        if data_type == wd1:
            self.data_array[self.active_data_index] = (variable, int(data), self.active_data_index)
        if data_type == wd2:
            data = float(data)
            data = f"{data:.2f}"
            data = float(data)
            scaled_data = int(data * (2 ** 7))
            self.data_array[self.active_data_index] = (variable, scaled_data, self.active_data_index)
        self.active_data_index = self.active_data_index + 1

    def decode_instruction(self, ins):
        tokens_a = ins.replace(";", "").replace(":", "").strip().split()
        if not tokens_a or len(tokens_a) < 5 or tokens_a[1] != "=":
            return "NOP 0 0 0 0"

        store_reg = tokens_a[0]
        op_1 = tokens_a[2]
        op_2 = tokens_a[4]
        operator = tokens_a[3]
        equator = tokens_a[1]

        if equator == "=":
            task = self.OPERATORS[operator]
            in_1 = self.data_array['address'][self.data_array['variable'] == op_1]
            in_2 = self.data_array['address'][self.data_array['variable'] == op_2]
            out = self.data_array['address'][self.data_array['variable'] == store_reg]

            if len(in_1) == 0 or len(in_2) == 0 or len(out) == 0:
                return "Error: One of the variables was not found in data_array"

            reg_a = 'R' + str(in_1[0])
            reg_b = 'R' + str(in_2[0])
            reg_out = 'R' + str(out[0])
            return f"{task} {reg_a} {reg_b} {reg_out}"
        return "Error: Invalid syntax (missing '=')"

    def decode_condition(self, ins):
        tokens_a = ins.split()
        operator = tokens_a[2]
        op2 = tokens_a[3]
        op1 = tokens_a[1]
        tsk = self.OPERATORS[operator]
        in_1 = self.data_array['address'][self.data_array['variable'] == op1]
        in_2 = self.data_array['address'][self.data_array['variable'] == op2]
        if len(in_1) == 0 or len(in_2) == 0:
            return None
        rega = 'R' + str(in_1[0])
        regb = 'R' + str(in_2[0])
        return f"{tsk} {rega} {regb} R0"

    def compile(self):
        block_stack = []
        compiled_lines = []
        with open(r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\program.txt") as infile:
            lines = [l.strip() for l in infile if l.strip()]

            for line in lines:
                if "this is how" in line:
                    line = line.split("this is how")[0].strip()
                tokens = line.split()

                if tokens[0] in ["int", "float"]:
                    self.data_assign(line)
                    continue
                if tokens[0] == "if":
                    cond_asm = self.decode_condition(line)
                    block_stack.append({
                        'type': 'IF', 'cond_asm': cond_asm,
                        'start_pc': self.program_counter, 'body': []
                    })
                    self.program_counter += 4
                    continue
                elif tokens[0] == "while":
                    cond_asm = self.decode_condition(line)
                    block_stack.append({
                        'type': 'WHILE', 'cond_asm': cond_asm,
                        'start_pc': self.program_counter+1, 'body': []
                    })
                    self.program_counter += 4
                    continue


                if_end = len(block_stack) > 0 and block_stack[-1]['type'] == 'IF' and line == "endif"
                while_end = len(block_stack) > 0 and block_stack[-1]['type'] == 'WHILE' and line == "endwhile"

                if if_end or while_end:
                    finished_block = block_stack.pop()
                    block_asm = []

                    if finished_block['type'] == "IF":
                        jump_target = self.program_counter
                        block_asm.append(finished_block['cond_asm'])
                        block_asm.append(f"JUMP {jump_target+1}\nNOP 0 0 0 0\nNOP 0 0 0 0")
                        block_asm.extend(finished_block['body'])

                    elif finished_block['type'] == "WHILE":
                        jump_target = self.program_counter + 4
                        block_asm.append(finished_block['cond_asm'])
                        block_asm.append(f"JUMP {jump_target}\nNOP 0 0 0 0\nNOP 0 0 0 0")
                        block_asm.extend(finished_block['body'])
                        block_asm.append(f"JUMP {finished_block['start_pc']}\nNOP 0 0 0 0\nNOP 0 0 0 0")
                        self.program_counter += 3

                    assembled_block = "\n".join(block_asm)

                    if block_stack:

                        block_stack[-1]['body'].extend(assembled_block.split("\n"))
                    else:
                        compiled_lines.append(assembled_block)
                    continue


                decoded_line = self.decode_instruction(line)
                if block_stack:
                    block_stack[-1]['body'].append(decoded_line)
                    self.program_counter += 1
                else:
                    compiled_lines.append(decoded_line)
                    self.program_counter += 1

        with open(r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\data.mem", "w") as f1:
            for idx in range(1, self.active_data_index):
                f1.write(format(self.data_array[idx]['value'], "032b") + "\n")

        with open(r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\ASSEMBLY_code.txt", "w") as f2:
            f2.write("\n".join(compiled_lines) + "\n")

        print("Compilation Complete!")


if __name__ == "__main__":
    compiler = CustomCompiler()
    compiler.compile()
