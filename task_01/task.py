import os

from itertools import combinations


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1721
979
366
299
675
1456\
'''

def calculate_1(data):
    nums = [int(x) for x in data.split('\n')]

    pairs = combinations(nums, 2)

    for x, y in pairs:
        if x + y == 2020:
            return x * y


def calculate_2(data):
    nums = [int(x) for x in data.split('\n')]

    triples = combinations(nums, 3)

    for x, y, z in triples:
        if x + y + z == 2020:
            return x * y * z


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 514579
    assert calculate_2(TEST_DATA) == 241861950

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
