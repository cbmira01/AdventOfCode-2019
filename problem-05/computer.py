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
        print ("\nScript notice: Unknown addressing mode: ", mode)
        exit()
    return result

def getOpcode( memory, pc ):
    pad = '00000' + str(memory[pc])
    return int(pad[-2:])

def getParameters( memory, pc, operationClass ):
    pad = '00000' + str(memory[pc])

    if (operationClass == "ALU"):
        p1Value = readMemory(memory, memory[pc + 1], int(pad[-3]))
        p2Value = readMemory(memory, memory[pc + 2], int(pad[-4]))
        resultLocation = memory[pc + 3]
    elif (operationClass == "IO"):
        p1Value = readMemory(memory, memory[pc + 1], int(pad[-3]))
        p2Value = 0
        resultLocation = 0
    elif (operationClass == "JUMP"):
        p1Value = readMemory(memory, memory[pc + 1], int(pad[-3]))
        p2Value = readMemory(memory, memory[pc + 2], int(pad[-4]))
        resultLocation = 0
    else:
        print("\nUnimplemented operation class ", operationClass)
        exit()

    return (0, p1Value, p2Value, resultLocation)

def getAluParameters( memory, pc ):
    return getParameters( memory, pc, operationClass="ALU" )

def getIoParameters( memory, pc ):
    return getParameters( memory, pc, operationClass="IO" )

def getJumpParameters( memory, pc ):
    return getParameters( memory, pc, operationClass="JUMP" )

def noOp( memory, pc ):
    print("\nNo-op not implemented.")
    exit()
    return None

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

def opcodeLookup( opcode ):
    switcher = {
        0: "No-Op",
        1: "Add",
        2: "Multiply",
        3: "Input",
        4: "Output",
        5: "Jump If True",
        6: "Jump If False",
        7: "Less Than",
        8: "Equals",
        99: "Halt"
    }
    return switcher.get( opcode, "Invalid operation")

def cpu( program, startLocation, debug, dump ):

    memory = program.copy()
    pc = startLocation

    if (debug):
        print("In debug mode...")

    while True:
        opcode = getOpcode(memory, pc)

        if (debug):
            try:
                print("  PC", pc, ": ", memory[pc + 0], memory[pc + 1], memory[pc + 2], memory[pc + 3], end='' )
                print("  ", opcodeLookup(opcode))
            except IndexError:
                print("\nIndexError in debugging")
                exit()

        nextPc = int(doInstruction(memory, pc, opcode))
        if (nextPc < 0):
            break

        pc = nextPc

    if (dump):
        for p in range(0, len(memory)):
            if (p % 10 == 0):
                print("\nDump", p, ':  ', end='')
            print(memory[p], ' ', end='')

    return None