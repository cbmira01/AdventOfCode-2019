#--- Day 3: Crossed Wires, first part ---

def findDups(listA, listB):
    return list(set(listA) & set(listB))

def runDirection(direction):
    switcher = {
        "U": [1, 0],
        "D": [-1, 0],
        "R": [0, 1],
        "L": [0, -1],
    }
    return switcher.get(direction)

def makeTrace(wire):
    # trace is a list of tuples, and so can support set operations
    trace = [(0,0)]
    
    for wireElement in range(0, len(wire)):
        dir = runDirection(wire[wireElement][0])
        run = int(wire[wireElement][1:])
        
        for r in range(0, run):
            end = trace[-1]
            new = (end[0] + dir[0], end[1] + dir[1])
            trace.append(new)
            
    return trace

with open('input') as f:
    inputWireA = f.readline()
    inputWireB = f.readline()

# For testing...
#inputWireA = "R8,U5,L5,D3"
#inputWireB = "U7,R6,D4,L4"
#shouldBe = 6

#inputWireA = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
#inputWireB = "U62,R66,U55,R34,D71,R55,D58,R83"
#shouldBe = 159

#inputWireA = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
#inputWireB = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
#shouldBe = 135

traceA = makeTrace([str(x) for x in inputWireA.split(",")])
traceB = makeTrace([str(x) for x in inputWireB.split(",")])

crossings = findDups(traceA, traceB)

while True:
    try:
        crossings.remove((0,0))
    except ValueError:
        break
            
print("All crossings: ", crossings)
print("Minimal distance: ", min((abs(c[0]) + abs(c[1])) for c in crossings[1:]))   
    
