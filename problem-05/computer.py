#--- Ship computer for problem 5 parts 1 and 2 ---

def writeMemory( memory, location, value ):
    try:
        memory[location] = value
    except IndexError:
        print("\nIndexError in writeMemory")
        exit()
    return None

def readMemory( memory, parameterValue, mode ):
    if (mode == 0): # position mode
        try:
            result = memory[parameterValue]
        except IndexError:
            print("\nIndexError in readMemory")
            exit()
    elif (mode == 1): # immediate mode
        result = parameterValue
    else:
        print ("\nUnimplemented addressing mode: ", mode)
        exit()
    return result

def getOpcode( memory, pc ):
    pad = '00000' + str(memory[pc])
    return int(pad[-2:])

def getParameters( memory, pc, operationClass ):
    pad = '00000' + str(memory[pc])
    p1Mode = int(pad[-3])
    p2Mode = int(pad[-4])

    if (operationClass == "ALU"):
        p1Value = readMemory(memory, memory[pc + 1], p1Mode)
        p2Value = readMemory(memory, memory[pc + 2], p2Mode)
        resultLocation = memory[pc + 3]
    elif (operationClass == "IO"):
        p1Value = readMemory(memory, memory[pc + 1], p1Mode)
        p2Mode = -1
        p2Value = 0
        resultLocation = 0
    elif (operationClass == "JUMP"):
        p1Value = readMemory(memory, memory[pc + 1], p1Mode)
        p2Value = readMemory(memory, memory[pc + 2], p2Mode)
        resultLocation = 0
    elif (operationClass == "HALT"):
        p1Mode = -1
        p1Value = 0
        p2Mode = -1
        p2Value = 0
        resultLocation = 0
    else:
        print("\nUnimplemented operation class ", operationClass)
        exit()

    return (0, p1Value, p2Value, resultLocation, p1Mode, p2Mode)

def getAluParameters( memory, pc ):
    return getParameters( memory, pc, operationClass="ALU" )

def getIoParameters( memory, pc ):
    return getParameters( memory, pc, operationClass="IO" )

def getJumpParameters( memory, pc ):
    return getParameters( memory, pc, operationClass="JUMP" )

def getHaltParameters( memory, pc ):
    return getParameters( memory, pc, operationClass="HALT" )

def noOp( memory, pc ):
    print("\nNo-op not implemented")
    exit()
    return -1

def addOp( memory, pc ):
    p = getAluParameters( memory, pc )
    writeMemory(memory, p[3], p[1] + p[2])
    return pc + 4

def multiplyOp( memory, pc ):
    p = getAluParameters( memory, pc )
    writeMemory(memory, p[3], p[1] * p[2])
    return pc + 4

def inputOp( memory, pc ):
    value = int(input("Enter an integer: "))
    writeMemory(memory, memory[pc + 1], value)
    return pc + 2

def outputOp( memory, pc ):
    p = getIoParameters( memory, pc )
    print("CPU Output: ", p[1])
    return pc + 2

def jumpIfTrueOp( memory, pc ):
    p = getJumpParameters(memory, pc)
    if (p[1] != 0):
        result = p[2]
    else:
        result = pc + 3
    return result

def jumpIfFalseOp( memory, pc ):
    p = getJumpParameters(memory, pc)
    if (p[1] == 0):
        result = p[2]
    else:
        result = pc + 3
    return result

def lessThanOp( memory, pc ):
    p = getAluParameters( memory, pc )
    if (p[1] < p[2]):
        writeMemory(memory, p[3], 1)
    else:
        writeMemory(memory, p[3], 0)
    return pc + 4

def equalsOp( memory, pc ):
    p = getAluParameters( memory, pc )
    if (p[1] == p[2]):
        writeMemory(memory, p[3], 1)
    else:
        writeMemory(memory, p[3], 0)
    return pc + 4

def haltOp( memory, pc ):
    p = getHaltParameters( memory, pc )
    print ("\nNormal halt at program counter", pc)
    return -1

def invalidOp( memory, pc ):
    print ("\nHalting on invalid operation", memory[pc + 0], " at program counter", pc )
    return -1

def doInstruction( memory, pc, opcode ):
    if (opcode == 0):
        result = noOp(memory, pc)
    elif (opcode == 1):
        result = addOp(memory, pc)
    elif (opcode == 2):
        result = multiplyOp(memory, pc)
    elif (opcode == 3):
        result = inputOp(memory, pc)
    elif (opcode == 4):
        result = outputOp(memory, pc)
    elif (opcode == 5):
        result = jumpIfTrueOp(memory, pc)
    elif (opcode == 6):
        result = jumpIfFalseOp(memory, pc)
    elif (opcode == 7):
        result = lessThanOp(memory, pc)
    elif (opcode == 8):
        result = equalsOp(memory, pc)
    elif (opcode == 99):
        result = haltOp(memory, pc)
    else:
        result = invalidOp(memory, pc)
    return result

def opcodeTable( opcode ):
    switcher = {
        0: "NOP,HALT",
        1: "ADD,ALU",
        2: "MULT,ALU",
        3: "INP,IO",
        4: "OUT,IO",
        5: "JT,JUMP",
        6: "JF,JUMP",
        7: "LT,ALU",
        8: "EQ,ALU",
        99: "HALT,HALT"
    }
    return switcher.get( opcode, "Invalid operation,0,0")

def getProtected( list, p ):
    try:
        result = list[p]
    except IndexError:
        result = 0 # default
    return result

def parameterDisplay(n, mode):
    return str(n) if mode == 1 else "[" + str(n) + "]"

def debugFetchAndDecode( memory, pc, opcode ):
    ocLookup = opcodeTable(opcode)
    ocName = ocLookup.split(",")[0]
    ocClass = ocLookup.split(",")[1]

    pc0 = getProtected(memory, pc)
    pc1 = getProtected(memory, pc + 1)
    pc2 = getProtected(memory, pc + 2)
    pc3 = getProtected(memory, pc + 3)
    
    sp = "." * 5

    print(f"  PC {pc:4}: ", end='' )
    if (ocClass == "HALT"):
        print(f"{pc0:5} {sp} {sp} {sp}", end='' )
        print(f"    {ocName}")
    if (ocClass == "IO"):
        print(f"{pc0:5} {pc1:5} {sp} {sp}", end='' )
        par = getParameters(memory, pc, ocClass)
        pc1Disp = parameterDisplay(pc1, par[4])
        print(f"    {ocName} {pc1Disp}")
    if (ocClass == "JUMP"):
        print(f"{pc0:5} {pc1:5} {pc2:5} {sp}", end='' )
        par = getParameters(memory, pc, ocClass)
        pc1Disp = parameterDisplay(pc1, par[4])
        pc2Disp = parameterDisplay(pc2, par[5])
        print(f"    {ocName} {pc1Disp} --> {pc2Disp} else continue")
    if (ocClass == "ALU"):
        print(f"{pc0:5} {pc1:5} {pc2:5} {pc3:5}", end='' )
        par = getParameters(memory, pc, ocClass)
        pc1Disp = parameterDisplay(pc1, par[4])
        pc2Disp = parameterDisplay(pc2, par[5])
        pc3Disp = parameterDisplay(pc3, 0) # always postion mode
        print(f"    {ocName} {pc1Disp} {pc2Disp} --> {pc3Disp}")

def cpu( program, startLocation, debug, dump ):
    memory = program.copy()
    pc = startLocation

    if (debug):
        print("In debug mode...")

    while True:
        opcode = getOpcode(memory, pc)

        if (debug):
            debugFetchAndDecode(memory, pc, opcode)

        nextPc = int(doInstruction(memory, pc, opcode))
        if (nextPc < 0):
            break

        pc = nextPc

    if (dump):
        for p in range(0, len(memory)):
            if (p % 10 == 0):
                print(f"\nDump {p:4}:  ", end='')
            print(f"{memory[p]:5} ", end='')

    return None