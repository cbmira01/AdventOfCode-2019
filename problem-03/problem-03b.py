#--- Day 3: Crossed Wires, second part ---
        
def findCrossings(wireA, wireB):

    wireSetA = set([(a,b) for (a,b,c) in wireA])
    wireSetB = set([(a,b) for (a,b,c) in wireB])
    crosses = list(wireSetA & wireSetB)
    
    while True:
        try:
            crosses.remove((0, 0))
        except ValueError:
            break

    result = []
    for c in crosses:
        wA = [wa for wa in wireA if wa[0] == c[0] and wa[1] == c[1]]
        wB = [wb for wb in wireB if wb[0] == c[0] and wb[1] == c[1]]
        result.append((c[0], c[1], wA[0][2] + wB[0][2]))

    return result

def runDirection(direction):
    switcher = {
        "U": [1, 0],
        "D": [-1, 0],
        "R": [0, 1],
        "L": [0, -1],
    }
    return switcher.get(direction)

def renderWire(rawWire):

    wire = [str(x) for x in rawWire.split(",")]    
    trace = [(0, 0, 0)]
    
    for wireElement in range(0, len(wire)):
        
        dir = runDirection(wire[wireElement][0])
        run = int(wire[wireElement][1:])
        
        for r in range(0, run):
            eow = trace[-1]
            newTrace = (eow[0] + dir[0], eow[1] + dir[1], eow[2] + 1)
            trace.append(newTrace)

    return trace

with open('input') as f:
    inputWireA = f.readline()
    inputWireB = f.readline()

# For testing...
#inputWireA = "R8,U5,L5,D3"
#inputWireB = "U7,R6,D4,L4"
# Minimal crossing distance 6
# Minimal combined run length: 30

#inputWireA = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
#inputWireB = "U62,R66,U55,R34,D71,R55,D58,R83"
# Minimal crossing distance 159
# Minimal combined run length: 610

#inputWireA = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
#inputWireB = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
# Minimal crossing distance 135
# Minimal combined run length: 410

crossings = findCrossings(renderWire(inputWireA), renderWire(inputWireB))
   
print("All crossings and distances: ", crossings)
print("Minimal origin distance: ", min((abs(c[0]) + abs(c[1])) for c in crossings))
print("Minimal run distance: ", min(c[2] for c in crossings))
    