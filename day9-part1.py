import sys


def S(a: int, b: int) -> int:
    # sum a range of numbers from [a, b] inclusive
    return int(((b - a + 1) / 2) * (a + b))


with open(sys.argv[1]) as f:
    data = f.read().strip()

diskmap = list(map(int, list(data)))

# if there's free space in the end, we can just throw it away
if len(diskmap) % 2 == 0:
    diskmap.pop()

head = 0
tail = len(diskmap) - 1
idx = 0

sum = 0
while head < tail:
    if head % 2 == 0:
        assert diskmap[head] > 0  # making an assumption here
        diff = S(idx, idx + diskmap[head] - 1) * (head // 2)
        sum += diff
        idx += diskmap[head]
        diskmap[head] = 0
        head += 1

    elif diskmap[head] == 0:
        # free space block but no space
        head += 1

    elif diskmap[head] >= diskmap[tail]:
        assert head % 2 != 0  # ensure free space
        assert tail % 2 == 0  # ensure tail file block
        # free space and enough to accomodate end
        diff = S(idx, idx + diskmap[tail] - 1) * (tail // 2)
        sum += diff
        idx += diskmap[tail]
        diskmap[head] -= diskmap[tail]
        diskmap[tail] = 0
        tail -= 2  # 2 since we skip the free space

    else:
        assert diskmap[head] < diskmap[tail]
        assert head % 2 != 0  # ensure free space
        assert tail % 2 == 0  # ensure tail file block
        diff = S(idx, idx + diskmap[head] - 1) * (tail // 2)
        sum += diff
        idx += diskmap[head]
        diskmap[tail] -= diskmap[head]
        diskmap[head] = 0
        head += 1

# there may be one left over cell
if head % 2 == 0:
    assert diskmap[head] > 0
    diff = S(idx, idx + diskmap[head] - 1) * (head // 2)
    sum += diff
    idx += diskmap[head]
    diskmap[head] = 0
    head += 1

print(sum)
