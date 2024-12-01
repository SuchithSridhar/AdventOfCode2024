import sys

with open(sys.argv[1]) as f:
    data = f.read()

leftList, rightList = zip(*[map(int, line.split("   ")) for line in data.splitlines()])
diff = sum(
    abs(left - right) for left, right in zip(sorted(leftList), sorted(rightList))
)
print(diff)
