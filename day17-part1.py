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


class Computer:
    ISA_STR = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
    ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = 0, 1, 2, 3, 4, 5, 6, 7
    ISA = [ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV]

    def __init__(self, program: list[int], reg_A: int, reg_B: int, reg_C: int):
        self.program = program
        self.output: list[int] = []
        self.A = reg_A
        self.B = reg_B
        self.C = reg_C
        self.ip = 0

    def adv(self, operand):
        operand = self.eval_combo_operand(operand)
        self.A = int(self.A / (2**operand))

    def bxl(self, operand):
        self.B = self.B ^ operand

    def bst(self, operand):
        operand = self.eval_combo_operand(operand)
        self.B = operand % 8

    def jnz(self, operand):
        if self.A != 0:
            self.ip = operand
        else:
            self.ip += 2

    def bxc(self, _):
        self.B = self.B ^ self.C

    def out(self, operand):
        operand = self.eval_combo_operand(operand)
        self.output.append(operand % 8)

    def bdv(self, operand):
        operand = self.eval_combo_operand(operand)
        self.B = int(self.A / (2**operand))

    def cdv(self, operand):
        operand = self.eval_combo_operand(operand)
        self.C = int(self.A / (2**operand))

    def eval_combo_operand(self, operand) -> int:
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        else:
            raise ValueError("Invalid combo operand.")

    def simulate(self) -> list[int]:
        while (self.ip + 1) < len(self.program):
            opcode = self.program[self.ip]
            operand = self.program[self.ip + 1]

            match opcode:
                case self.ADV:
                    self.adv(operand)
                case self.BXL:
                    self.bxl(operand)
                case self.BST:
                    self.bst(operand)
                case self.JNZ:
                    self.jnz(operand)
                case self.BXC:
                    self.bxc(operand)
                case self.OUT:
                    self.out(operand)
                case self.BDV:
                    self.bdv(operand)
                case self.CDV:
                    self.cdv(operand)
                case _:
                    raise ValueError(f"Unknown opcode: {opcode}")

            if opcode != self.JNZ:
                self.ip += 2

        return self.output


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

    computer = Computer(program, reg_a, reg_b, reg_c)
    output = computer.simulate()

    print(",".join(list(map(str, output))))


if __name__ == "__main__":
    main()
