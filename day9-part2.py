import sys


class DataBlk:
    def __init__(self, blkid, idx, length) -> None:
        self.bid = blkid
        self.idx = idx
        self.len = length

    def sum(self) -> int:
        # sum a range of numbers from [a, b] inclusive
        end = self.idx + self.len - 1
        return self.bid * int(((self.len) / 2) * (self.idx + end))


class FreeBlk:
    def __init__(self, idx, length) -> None:
        self.idx = idx
        self.len = length


def find_free_block(db: DataBlk, fbl: list[list[FreeBlk]]) -> int:
    min = db.idx
    fbli = -1
    for i in range(db.len, len(fbl)):
        if len(fbl[i]) > 0 and fbl[i][0].idx < min:
            min = fbl[i][0].idx
            fbli = i

    return fbli


def insert_free_block(fb: FreeBlk, fbl: list[list[FreeBlk]]):
    if fb.len <= 0:
        return

    sub = fbl[fb.len]

    # we need to insert it in the right spot using binary search
    left, right = 0, len(sub) - 1
    while left <= right:
        mid = (left + right) // 2
        if sub[mid].idx < fb.idx:
            left = mid + 1
        else:
            right = mid - 1

    sub.insert(left, fb)


with open(sys.argv[1]) as f:
    data = f.read().strip()

diskmap = list(map(int, list(data)))

# if there's free space in the end, we can just throw it away
if len(diskmap) % 2 == 0:
    diskmap.pop()


# we only need 9 but I take 10 to make indexing easier
free_blocks: list[list[FreeBlk]] = [[] for _ in range(10)]
data_blocks: list[DataBlk] = []
idx = 0

for i, size in enumerate(diskmap):
    if i % 2 == 0:
        data_blocks.append(DataBlk(i // 2, idx, size))
    else:
        free_blocks[size].append(FreeBlk(idx, size))
    idx += size

for i in range(len(data_blocks) - 1, 0, -1):
    free_blk_id = find_free_block(data_blocks[i], free_blocks)
    if free_blk_id == -1:
        # no block was found
        continue

    # we replace the free block with the data block
    free_block = free_blocks[free_blk_id].pop(0)
    data_blocks[i].idx = free_block.idx
    free_block.len = free_block.len - data_blocks[i].len
    free_block.idx += data_blocks[i].len
    # there may be some left over free space
    insert_free_block(free_block, free_blocks)

sum = 0
for blk in data_blocks:
    sum += blk.sum()

print(sum)
