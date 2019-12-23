# --- Day 1: The Tyranny of the Rocket Equation, second part ---
import math

def fuelNeeded(mass):
    return math.floor(float(mass) / 3) - 2

input_file = open('input', 'r')

fuelTotal = 0

for line in input_file:
    moduleMass = int(line)
    fuelSubtotal = 0    
    fuelMass = fuelNeeded(moduleMass)

    while True:
        fuelSubtotal = fuelSubtotal + fuelMass
        fuelMass = fuelNeeded(fuelMass)
        if (fuelMass <= 0):
            break

    fuelTotal = fuelTotal + fuelSubtotal
    
print (fuelTotal, end='')  
  