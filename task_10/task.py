import os

from itertools import combinations


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
16
10
15
5
1
11
7
19
6
12
4\
'''

def calculate_1(data):
    adapters = list(map(int, data.split('\n')))

    device_joltage = max(adapters) + 3

    print([a for a in adapters if a - 1 <= 3])


def calculate_2(data):
    pass


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 35
    # assert calculate_2(TEST_DATA) == 241861950

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    # answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    # print(f'{answer_2=}')
