# --- Day 1: The Tyranny of the Rocket Equation ---
import math

fuelTotal= 0

input_file = open('input', 'r')
count_lines = 0
for line in input_file:
    #print (line, end = '')
    #count_lines += 1
    mass = float(line)
    fuelNeeded = math.floor(mass / 3) - 2
    fuelTotal = fuelTotal + fuelNeeded
    
print (fuelTotal, end='')  
  