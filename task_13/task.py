import os

from functools import reduce


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
939
7,13,x,x,59,x,31,19\
'''

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def decode_input(data):
    lines = data.split('\n')
    yield int(lines.pop(0))     # time
    yield lines.pop().split(',')


def calculate_1(data):
    decoder = decode_input(data)
    earliest_time = next(decoder)
    buses = [int(x) for x in next(decoder) if x != 'x']

    next_time = [bus - (earliest_time % bus) for bus in buses]
    next_earliest = min(next_time)
    next_bus = buses[next_time.index(next_earliest)]

    return next_bus * next_earliest


def calculate_2(data):
    decoder = decode_input(data)
    next(decoder)   # this is no longer relevant
    buses_paired = [(i, int(x)) for i, x in enumerate(next(decoder)) if x != 'x']

    buses = [b for i, b in buses_paired]
    offsets = [b - i for i, b in buses_paired]

    # After bashing my head for several hours, I just came to the following
    # conclusion:
    #
    #   (t + i) mod bus = 0
    #
    # the above holds for a certain t for _all_ the buses!
    # However I could not come up with a way for finding out how to get that t.
    # For small numbers we can just use brute force, iterating from 1 to ...
    # But this is not optimal and you'll never reach a solution for bigger input
    # So... I cheated. Unfortuantely I am no mathematician, and I wanted to
    # just move on.
    #
    # I found a solution here: https://0xdf.gitlab.io/adventofcode2020/13
    #
    # And the code is pretty easy, except I still do not understand the algo.
    # What I do recall is using LCM/GCD to find such solutions.
    # Adding to to-read/to-figure-out list I guess!
    return chinese_remainder(buses, offsets)


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 295
    assert calculate_2(TEST_DATA) == 1068781

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
