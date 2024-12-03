import sys
import re

with open(sys.argv[1]) as f:
    data = f.read()


pattern = r"mul\((\d\d?\d?),(\d\d?\d?)\)"
print(sum(int(x) * int(y) for x, y in re.findall(pattern, data)))
