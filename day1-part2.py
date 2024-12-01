import sys

with open(sys.argv[1]) as f:
    data = f.read()

rightMap = {}
leftSet = set()
for line in data.splitlines():
    left, right = map(int, line.split("   "))
    leftSet.add(left)
    if right in rightMap:
        rightMap[right] += 1
    else:
        rightMap[right] = 1

similarityScore = 0
for number, count in rightMap.items():
    if number in leftSet:
        similarityScore += number * count

print(similarityScore)
