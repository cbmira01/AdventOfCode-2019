#--- Day 2: 1202 Program Alarm, second part ---

def runProgram( program, noun, verb, startLoc ):  
    mem = program.copy()
    mem[1] = noun
    mem[2] = verb
    pc = startLoc
    while True:
        instr = mem[pc]
        op1_loc = mem[pc + 1]
        op2_loc = mem[pc + 2]
        result_loc = mem[pc + 3]
        
        if instr == 1:
            mem[result_loc] = mem[op1_loc] + mem[op2_loc]
        elif instr == 2:
            mem[result_loc] = mem[op1_loc] * mem[op2_loc]
        elif instr == 99:
            result = mem[0]
            break
        else:
            result = -1
            break
        
        pc = pc + 4
        
    return result

with open('input') as f:
    data = f.read()   

program = [int(x) for x in data.split(",")]
soughtResult = 19690720

for noun in range(0, 100):
    breaker = False
    for verb in range(0, 100):        
        result = runProgram(program, noun, verb, 0)
        #print ("Noun = ", noun, ", verb = ", verb, ", result = ", result)
        
        if (result != soughtResult): 
            continue
        else:
            print ("Result found! Noun = ", noun, ", verb = ", verb)
            breaker = True
            break
    if (breaker):
        break