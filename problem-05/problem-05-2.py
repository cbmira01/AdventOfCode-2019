#--- Problem 5, part 2 ---

import computer

with open('input') as f:
    data = f.read()  

program = [int(x) for x in data.split(",")]

computer.cpu( program, 0, True, True)

#computer.cpu( program, 0, False, False)
