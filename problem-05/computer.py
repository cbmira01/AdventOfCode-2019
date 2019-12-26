#--- Ship computer sufficient for problem 5 ---
#
# - supports console I/O
# - supports immediate and position parameter modes
# - has debug and dump flags
#

def writeBack(memory, location, value):
    memory[location] = value
    return None

def loadByMode(memory, parameterValue, mode):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    if (mode == POSITION_MODE):
        result = memory[parameterValue]
    elif (mode == IMMEDIATE_MODE):
        result = parameterValue
    else:
        print ("Unknown addressing mode: ", mode)
        exit()

    return result

def parseInstruction( memory, pc ):
    paddedInstruction = '00000' + str(memory[pc])
    instruction = {}

    opcode = int(paddedInstruction[-2:])
    instruction["opcode"] = opcode

    if (opcode == 1):
        instruction["op"] = "Add"
        instruction["opClass"] = "Arithmetic"
    elif (opcode == 2):
        instruction["op"] = "Multiply"
        instruction["opClass"] = "Arithmetic"
    elif (opcode == 3):
        instruction["op"] = "Input"
        instruction["opClass"] = "Input-Output"
    elif (opcode == 4):
        instruction["op"] = "Output"
        instruction["opClass"] = "Input-Output"
    elif (opcode == 99):
        instruction["op"] = "Halt"
        instruction["opClass"] = "Control"
    else:
        instruction["op"] = "Illegal operation"

    instruction["p1Mode"] = None
    instruction["p1Value"] = None
    instruction["p2Mode"] = None
    instruction["p2Value"] = None
    instruction["resultLocation"] = None
    instruction["increment"] = None

    if (instruction["opClass"] == "Input-Output"):
        instruction["resultLocation"] = memory[pc + 1]
        instruction["increment"] = 2
    elif (instruction["opClass"] == "Control"):
        instruction["increment"] = 0
    elif (instruction["opClass"] == "Arithmetic"):
        instruction["p1Mode"] = int(paddedInstruction[-3])
        instruction["p1Value"] = loadByMode(memory, memory[pc + 1], instruction["p1Mode"])
        instruction["p2Mode"] = int(paddedInstruction[-4])
        instruction["p2Value"] = loadByMode(memory, memory[pc + 2], instruction["p2Mode"])
        instruction["resultLocation"] = memory[pc + 3]
        instruction["increment"] = 4
    else:
        print("Operation class not implemented.")
        exit()

    return instruction

def cpu( program, startLocation, debug, dump ):

    memory = program.copy()
    pc = startLocation

    if (debug):
        print("In debug mode...")

    while True:
        instruction = parseInstruction(memory, pc)
        opcode = instruction["opcode"]

        if (debug):
            print("  ", pc, ": ", memory[pc + 0], memory[pc + 1], memory[pc + 2], memory[pc + 3], end='' )
            print("  ", instruction["op"], instruction["p1Value"], instruction["p2Value"], " --> ", instruction["resultLocation"])

        if (instruction["op"] == "Add"):
            value = instruction["p1Value"] + instruction["p2Value"]
            writeBack(memory, instruction["resultLocation"], value)
        elif (instruction["op"] == "Multiply"):
            value = instruction["p1Value"] * instruction["p2Value"]
            writeBack(memory, instruction["resultLocation"], value)
        elif (instruction["op"] == "Input"):
            intValue = int(input("Enter an integer: "))
            writeBack(memory, instruction["resultLocation"], intValue)
        elif (instruction["op"] == "Output"):
            print("CPU Output: ", memory[instruction["resultLocation"]])
        elif (instruction["op"] == "Halt"):
            print ("Normal halt at program counter ", pc, ", diagnostic code = ", memory[pc + 1])
            break
        else:
            print ("Halted on illegal instruction: ", instruction)
            break

        pc = pc + instruction["increment"]

    if (dump):
        for p in range(0, len(memory)):
            if (p % 10 == 0):
                print("\nDump", p, ':  ', end='')
            print(memory[p], ' ', end='')

    return None