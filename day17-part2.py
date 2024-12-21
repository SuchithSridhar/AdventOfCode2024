import sys
import re


# 3-bit compute, making list of 3-bit numbers (0 to 7)
# IP increments by 2 after each instruction
# 0,1,2,3 -> 0 opcode and 1 operand. then 2 opcode and 3 operand
# two types of operand, literal and combo:
# combo meanings:
# 0 - 3 -> literal
# 4 -> reg A
# 5 -> reg B
# 6 -> reg C
# 7 -> not valid

# Instructions
# 0 -> adv -> division reg A / 2^(combo op)    # truncated and stored in Reg A
# 1 -> bxl -> bitwise XOR of reg B and literal op  # Store in B
# 2 -> bst -> combo op % 8    # store in B
# 3 -> jnz -> f A != 0  jump to literal operand
# 4 -> bxc -> bitwise XOR of B and C and store in B   (read op but ignore)
# 5 -> out -> combo op % 8 and output value
# 6 -> bdv -> div reg A / 2^(combo op)     # truncated and stored in Reg B
# 7 -> cdv -> div reg A / 2^(combo op)     # truncated and stored in Reg C


# for my input these were the instructions:
# Program: [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]
# Reg A: 44348299
# Reg B: 0
# Reg C: 0
# 0: bst A
# 1: bxl 5
# 2: cdv B
# 3: bxl 6
# 4: adv 3
# 5: bxc 2
# 6: out B
# 7: jnz 0

# This works out to be the following:
# 0. B = last 3 bit of A
# 1. B = B XOR 5 (101)
# 2. C = A >> B
# 3. B = B XOR 6 (110)
# 4. A = A >> 3     (delete last three bits of A)
# 5. B = B ^ C
# 6. O = B % 8      (select last 3 bits) equivalent to just B
# 7. Jump to start


def find_hardcoded(a_value, index, program):
    if index == -1:
        return a_value
    for b in range(8):
        # make space for the next 3 bits
        # add the chosen 3 bits
        a = (a_value << 3) + b
        b = a % 8
        b = b ^ 5
        c = a >> b
        b = b ^ 6
        b = b ^ c
        if b % 8 == program[index]:
            if (x := find_hardcoded(a, index - 1, program)) is not None:
                return x
            else:
                continue
    return None


def print_ops(program):
    ISA_STR = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
    OP_COM = ["0", "1", "2", "3", "A", "B", "C"]
    COM_ISA = [0, 2, 5, 6, 7]
    for i in range(0, len(program), 2):
        op, od = program[i], program[i + 1]
        ods = OP_COM[od] if op in COM_ISA else str(od)
        print(f"{i//2}: {ISA_STR[op]} {ods}")


def main():
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    pattern = r".*A: (\d+).*B: (\d+).*C: (\d+).*Program: ([\d,]+).*"
    match = re.search(pattern, data, re.DOTALL)
    assert match
    reg_a = int(match.group(1))
    reg_b = int(match.group(2))
    reg_c = int(match.group(3))
    program = list(map(int, match.group(4).split(",")))

    print("Program:", program)
    print("Reg A:", reg_a)
    print("Reg B:", reg_b)
    print("Reg C:", reg_c)

    print_ops(program)
    print("Found A:", find_hardcoded(0, len(program) - 1, program))


if __name__ == "__main__":
    main()
