import numpy as np
my_structure=np.dtype([
    ('variable','U10'),
    ('value','i4'),
    ('address','i4')
])
data_array=np.zeros(255,dtype=my_structure)
data_array[0]=('ZZ',0,0)


def data_assign(instructions,active_index):
   tokens=instructions.split()
   data_type=tokens[0]
   variable=tokens[1]
   data=tokens[3]
   wd1="int"
   wd2="float"

   if data_type==wd1 :
         data_array[active_index]=(variable,int(data),active_index)
   if data_type==wd2 :
         data=float(data)
         data=f"{data:.2f}"
         data=float(data)
         scaled_data = int(data * (2 ** 7))
         data_array[active_index] = (variable, scaled_data, active_index)




OPERATORS={
    "+":"ALU_EN ADD",
    "-":"ALU_EN SUB",
    "*":"ALU_EN MUL",
    "&":"ALU_EN AND",
    "^":"ALU_EN XOR",
    "|":"ALU_EN OR ",
    ">":"ALU_EN GREATER",
    "<":"ALU_EN LESS",
    "==":"ALU_EN EQUAL"

}

def instruction_decode(ins) :
    tokens_a=ins.split()
    if not tokens_a:
        return "Empty instruction"

    store_reg=tokens_a[0]
    op_1=tokens_a[2]
    op_2=tokens_a[4]
    operator=tokens_a[3]
    equator=tokens_a[1]


    if equator == "=":
        task=OPERATORS[operator]
        in_1=data_array['address'][data_array['variable'] == op_1]
        in_2=data_array['address'][data_array['variable'] == op_2]
        out=data_array['address'][data_array['variable'] == store_reg]

        if len(in_1) == 0 or len(in_2) == 0 or len(out) == 0:
            return "Error: One of the variables was not found in data_array"

        reg_a='R'+str(in_1[0])
        reg_b='R'+str(in_2[0])
        reg_out='R'+str(out[0])
        assembly_ins=task+" "+reg_a+" "+reg_b+" "+reg_out
        return assembly_ins
    return "Error: Invalid syntax (missing '=')"
final_string=""
if_blk=""

def if_block(ins):
    global final_string
    global if_blk

    tokens_z=ins.split()
    if tokens_z[0]=="if" :
        op1=tokens_z[1]
        operator=tokens_z[2]
        op2=tokens_z[3]

        tsk=OPERATORS[operator]
        in1 = data_array['address'][data_array['variable'] == op1]
        in2 = data_array['address'][data_array['variable'] == op2]
        ink=0
        if len(in1) == 0 or len(in2) == 0:
            if_blk = "Error: If-condition variables not found\n"
            return
        rega= 'R' + str(in1[0])
        regb = 'R' + str(in2[0])
        rego = 'R' + str(ink)

        instruct=tsk+" "+rega+" "+regb+" "+rego
        if_blk = instruct + "\n"



    if tokens_z[-1]==";" :
         if not tokens_z:
             return "Empty instruction"

         store_reg = tokens_z[0]
         op_1 = tokens_z[2]
         op_2 = tokens_z[4]
         operator = tokens_z[3]
         equator = tokens_z[1]

         if equator == "=":
             task = OPERATORS[operator]
             in_1 = data_array['address'][data_array['variable'] == op_1]
             in_2 = data_array['address'][data_array['variable'] == op_2]
             out = data_array['address'][data_array['variable'] == store_reg]

             if len(in_1) == 0 or len(in_2) == 0 or len(out) == 0:
                 return "Error: One of the variables was not found in data_array"

             reg_a = 'R' + str(in_1[0])
             reg_b = 'R' + str(in_2[0])
             reg_out = 'R' + str(out[0])
             assembly_ins1 = task + " " + reg_a + " " + reg_b + " " + reg_out

             final_string+=assembly_ins1+"\n"

loop_blk=""
final_loop=""


def loop_block(ins):
    global loop_blk
    global final_loop


    tokens_l=ins.split()
    if tokens_l[0]=="while":
        ope1=tokens_l[1]
        comp=tokens_l[2]
        ope2=tokens_l[3]

        tsk_l=OPERATORS[comp]
        in1_l = data_array['address'][data_array['variable'] == ope1]
        in2_l = data_array['address'][data_array['variable'] == ope2]
        ink_l=0
        if len(in1_l) == 0 or len(in2_l) == 0:
            loop_blk = "Error: If-condition variables not found\n"
            return
        rega= 'R' + str(in1_l[0])
        regb = 'R' + str(in2_l[0])
        rego = 'R' + str(ink_l)

        instruct=tsk_l+" "+rega+" "+regb+" "+rego
        loop_blk = instruct + "\n"


    if tokens_l[-1] == ":":
        if not tokens_l:
            return "Empty instruction"

        store_regl = tokens_l[0]
        op_1l = tokens_l[2]
        op_2l = tokens_l[4]
        operatorl = tokens_l[3]
        equatorl = tokens_l[1]


        if equatorl == "=":
           task = OPERATORS[operatorl]
           in_1l= data_array['address'][data_array['variable'] == op_1l]
           in_2l = data_array['address'][data_array['variable'] == op_2l]
           outl = data_array['address'][data_array['variable'] == store_regl]

           if len(in_1l) == 0 or len(in_2l) == 0 or len(outl) == 0:
              return "Error: One of the variables was not found in data_array"

           reg_a = 'R' + str(in_1l[0])
           reg_b = 'R' + str(in_2l[0])
           reg_out = 'R' + str(outl[0])
           assembly_ins1 = task + " " + reg_a + " " + reg_b + " " + reg_out
           final_loop+=assembly_ins1+"\n"

i=1
k=0
z=0
count=0
with open(r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\program.txt","r") as infile:
    with open(r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\data.mem", "w") as f1, open(r"C:\Users\Diganta Biswas\OneDrive\microcontroller testing\ASSEMBLY_code.txt", "w") as f2:

        for line in infile:
           if not line.strip():
               continue
           tokens_x=line.strip().split()
           if tokens_x[0]=="int" or tokens_x[0]=="float" :

             data_assign(line.strip(),i)
             val = data_array[i]['value']
             f1.write(format(val,"032b")+"\n")
             i=i+1
             if i>255:
               break
           elif tokens_x[0]=="if" or tokens_x[-1]==";":
               if tokens_x[0] == "if":
                   k=count
                   k = k + 4
               if tokens_x[-1] ==";":
                   k = k + 1
               if_block(line.strip())
           elif if_blk!="":
                   if_blk = if_blk + "JUMP " + str(k) + "\n" + "NOP 0 0 0 0" + "\n" + "NOP 0 0 0 0" + "\n"

                   f2.write(if_blk+final_string)
                   count=k
                   final_string=""
                   if_blk=""

                   instruction=instruction_decode(line.strip())
                   if instruction is not None:
                     f2.write(instruction + "\n")
                     count=count+1
           elif tokens_x[0]=="while" or tokens_x[-1]==":":
               if tokens_x[0] == "while":
                   print(count)
                   z=count

                   z=z+4
               if tokens_x[-1] ==":":
                   z=z+1
               loop_block(line.strip())
           elif loop_blk!="":
                   loop_blk=loop_blk+"JUMP " + str(z+3) + "\n" + "NOP 0 0 0 0" + "\n" + "NOP 0 0 0 0" + "\n"
                   final_loop+="JUMP " + str(count) + "\n" + "NOP 0 0 0 0" + "\n" + "NOP 0 0 0 0" + "\n"
                   f2.write(loop_blk + final_loop)

                   count = z+3
                   final_loop = ""
                   loop_blk = ""

                   instruction = instruction_decode(line.strip())
                   if instruction is not None:
                       f2.write(instruction + "\n")
                       count=count+1
           elif tokens_x[0]!="if" or tokens_x[0]!="float" or tokens_x[0]!="int" or tokens_x[0]!="while":
                  instruction = instruction_decode(line.strip())
                  count=count+1
                  if instruction is not None:
                         f2.write(instruction + "\n")
        if if_blk!="" :
            f2.write(if_blk+final_string)
        if loop_blk!="":
            f2.write(loop_blk+final_loop)