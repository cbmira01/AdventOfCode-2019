#--- Problem 4, part 2 ---

def hasOnlyTwoAdjacent(n):
    s = str(n) + 'e'
    
    p = 0
    det = 1
    acc = str(det)
    while True:
        p = p + 1
        if (p >= 7):
            break
        if (s[p] == s[p-1]):
            det = det + 1            
        else:
            det = 1
        acc = acc + str(det)
    
    if (acc.find('121') >= 0):
        result = True
    else:
        result = False

    return result    

def isMonotonic(n):
    s = str(n)
    result = True

    for p in range(0, 5):
        if (s[p] > s[p+1]):
            result = False
            break

    return result

sum = 0
for n in range(123257, 647015 + 1):
    if (not isMonotonic(n)):
        continue
    if (not hasOnlyTwoAdjacent(n)):
        continue
    sum = sum + 1

print("Number of possible passwords:", sum)
