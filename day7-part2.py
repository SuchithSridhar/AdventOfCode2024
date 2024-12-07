import sys

# TODO: The numbers get big and while python can handle
# big inputs, we want to see if there's a nice clean way to handle it
# the final answer was: 145149066755184, which requies 43 bits to store.
# so may be int64 would have been enough.


def conc(lhs, rhs):
    copy = max(rhs, 1)  # ensure at least one move
    while copy != 0:
        lhs *= 10
        copy //= 10

    return lhs + rhs


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

    conc_value = eq_eval_recur((result, [conc(lhs, rhs)] + operands.copy()))
    if conc_value != 0:
        return conc_value

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
