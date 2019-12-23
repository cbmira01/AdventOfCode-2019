#--- Day 2: 1202 Program Alarm ---

with open('input') as f:
    data = f.read()   
#print (data, end='')

mainMemory = [int(x) for x in data.split(",")]
#print(mainMemory)

# mandatory preparation 
mainMemory[1] = 12
mainMemory[2] = 2
programCounter = 0

while True:
    instr = mainMemory[programCounter]
    op1_loc = mainMemory[programCounter + 1]
    op2_loc = mainMemory[programCounter + 2]
    result_loc = mainMemory[programCounter + 3]
    
    if instr == 1:
        mainMemory[result_loc] = mainMemory[op1_loc] + mainMemory[op2_loc]
    elif instr == 2:
        mainMemory[result_loc] = mainMemory[op1_loc] * mainMemory[op2_loc]
    elif instr == 99:
        print ("Normal halt; location 0 = ", mainMemory[0])  
        break
    else:
        print ("Illegal instruction, halted.", end='')
        break
    
    programCounter = programCounter + 4
