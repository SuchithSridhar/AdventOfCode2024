import sys


def trim(required, operand):
    return int(str(required)[: -len(str(operand))])


def ends_with(required, operand):
    return len(str(required)) > len(str(operand)) and str(required).endswith(
        str(operand)
    )


def eq_eval(equation):
    required, operands = equation
    return required if eq_eval_recur(required, operands) else 0


def eq_eval_recur(required, operands) -> bool:
    if len(operands) == 1:
        return required == operands[0]

    return (
        (
            required % operands[-1] == 0
            and eq_eval_recur(required // operands[-1], operands[:-1])
        )
        or (
            required > operands[-1]
            and eq_eval_recur(required - operands[-1], operands[:-1])
        )
        or (
            ends_with(required, operands[-1])
            and eq_eval_recur(trim(required, operands[-1]), operands[:-1])
        )
    )


with open(sys.argv[1]) as f:
    data = f.read().strip()

data = data.splitlines()
data = list(map(lambda x: x.split(": "), data))
data = [(int(r), list(map(int, ops.split(" ")))) for r, ops in data]

print(sum(map(eq_eval, data)))
