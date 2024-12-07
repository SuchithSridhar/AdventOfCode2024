import sys


# This worked but is slow (still instant but recursion)
# TODO: Try to do this without recursion
def eq_eval_recur(equation: tuple[int, list[int]]) -> int:
    result, operands = equation

    if len(operands) == 1:
        if operands[0] == result:
            return result
        else:
            return 0

    lhs = operands.pop(0)
    rhs = operands.pop(0)

    # small optimization
    if lhs > result or rhs > result:
        return 0

    add_value = eq_eval_recur((result, [lhs + rhs] + operands.copy()))
    if add_value != 0:
        return add_value

    mult_value = eq_eval_recur((result, [lhs * rhs] + operands.copy()))
    return mult_value


with open(sys.argv[1]) as f:
    data = f.read().strip()

data = data.splitlines()
data = list(map(lambda x: x.split(": "), data))
data = [(int(r), list(map(int, ops.split(" ")))) for r, ops in data]

print(sum(map(eq_eval_recur, data)))
