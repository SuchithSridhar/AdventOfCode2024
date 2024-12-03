import sys
import re

with open(sys.argv[1]) as f:
    data = f.read()


pattern = r"(mul\((\d\d?\d?),(\d\d?\d?)\)|do\(\)|don't\(\))"
# [('mul(2,4)', '2', '4'), ("don't()", '', ''), ('mul(5,5)', '5', '5'), ('mul(11,8)', '11', '8'), ('do()', '', ''), ('mul(8,5)', '8', '5')]

sum = 0
do = True
for op, x, y in re.findall(pattern, data):
    if do and op.startswith("mul"):
        sum += int(x) * int(y)
    else:
        do = op == "do()"

print(sum)
