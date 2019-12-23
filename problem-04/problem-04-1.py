#--- Problem 4, part 1 ---

def hasAdjacent(n):
    s = str(n)
    result = False

    for p in range(0, 5):
        if (s[p] == s[p+1]):
            result = True

    return result

def isMonotonic(n):
    s = str(n)
    result = True

    for p in range(0, 5):
        if (s[p] > s[p+1]):
            result = False

    return result

sum = 0
for n in range(123257, 647015 + 1):
    if (isMonotonic(n) and hasAdjacent(n)):
        sum = sum + 1

print("Number of possible passwords:", sum)
