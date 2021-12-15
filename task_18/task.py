import os
import operator
import ast


__here__ = os.path.dirname(__file__)

TEST_DATA_1 = '1 + 2 * 3 + 4 * 5 + 6'
TEST_DATA_2 = '1 + (2 * 3) + (4 * (5 + 6))'
TEST_DATA_3 = '2 * 3 + (4 * 5)'
TEST_DATA_4 = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'


OPS = {
    '+': operator.add,
    '*': operator.mul,
}

OPS_AST = {
    ast.Add: operator.mul,   # We flip the precedence, so these are mapped like this.
    ast.Mult: operator.add,
}


def solve_expr(expr):
    expr = expr.replace(' ', '')

    num_stack = []
    op_stack = []

    depth = 0

    for c in expr:
        if c.isnumeric():
            num_stack.append(int(c))
        elif c in '+*':
            op_stack.append(c)
            continue
        elif c == '(':
            op_stack.append(c)
        elif c == ')':
            op_stack.pop()

        if len(op_stack) and len(num_stack) >= 2:
            if op_stack[-1] == '(':
                continue
            rhs = num_stack.pop()
            lhs = num_stack.pop()
            op = op_stack.pop()

            num_stack.append(OPS[op](lhs, rhs))

    return num_stack.pop()

def solve_expr_advanced(expr):
    # This one cheats. Instead of trying to build a stack, we are
    # using the ast module built in python. Before we do that however,
    # we need to understand that ast parses expressions in standard
    # precedence rules. Since the rules are now different (MATH IS MATH)
    # we use a trick: We replace the multiplication which has higher
    # precedence in general, to addition, and addition to multiplication.
    # This means that generated ast is now using the same rules as we
    # want. This also means that in parsed result, ast.Add actually means
    # ast.Mult.
    # While evaluating the tree, we keep that fact in mind and apply the
    # correct operation.

    # Replace * with + and + with * to flip the precedence rule:
    expr = expr.replace('*', '@').replace('+', '*').replace('@', '+')

    # Get the ast for this expression.
    expr_parsed = ast.parse(expr, mode='eval')

    def evaluate_op(binop):
        # This is our exit condition:
        if type(binop) == ast.Constant:
            return binop.value

        if type(binop) == ast.BinOp:
            operator = OPS_AST[type(binop.op)]
            lhs = evaluate_op(binop.left)
            rhs = evaluate_op(binop.right)
            return operator(lhs, rhs)

    return evaluate_op(expr_parsed.body)


def calculate_1(data):
    lines = data.split('\n')
    val = 0
    for line in lines:
        val += solve_expr(line)
    return val


def calculate_2(data):
    lines = data.split('\n')
    val = 0
    for line in lines:
        val += solve_expr_advanced(line)
    return val


if __name__ == '__main__':
    assert calculate_1(TEST_DATA_1) == 71
    assert calculate_1(TEST_DATA_2) == 51
    assert calculate_1(TEST_DATA_3) == 26
    assert calculate_1(TEST_DATA_4) == 13632
    assert calculate_2(TEST_DATA_1) == 231
    assert calculate_2(TEST_DATA_2) == 51
    assert calculate_2(TEST_DATA_3) == 46
    assert calculate_2(TEST_DATA_4) == 23340

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
