from functools import cache
import sys


def ways_possible(design: str, towels: set[str]):
    max_towel = max(map(len, towels))

    @cache
    def recur(dsgn: str):
        if dsgn == "":
            return 1

        return sum(
            recur(dsgn[i:])
            for i in range(min(max_towel, len(dsgn)) + 1)
            if dsgn[:i] in towels
        )

    return recur(design)


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    towels, designs = data.split("\n\n")
    towels = set(towels.strip().split(", "))
    designs = designs.strip().split("\n")

    print(sum(ways_possible(design, towels) for design in designs))


if __name__ == "__main__":
    main()
