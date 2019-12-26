#--- Problem 5, part 1 ---

import computer

with open('input') as f:
    data = f.read()   

program = [int(x) for x in data.split(",")]

computer.cpu( program, 0, False, False)
