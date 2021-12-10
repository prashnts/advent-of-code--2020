import os

from collections import Counter
from functools import lru_cache


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
TEST_DATA_2 = '''\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3\
'''

def jolts_difference(adapters):
    device_joltage = max(adapters) + 3
    adapters_stack = sorted(adapters)
    # Insert wall socket at start.
    adapters_stack.insert(0, 0)
    # Insert final adapter
    adapters_stack.append(device_joltage)
    # Find the jolt differences
    diff = [b - a for a, b in zip(adapters_stack, adapters_stack[1:])]
    return adapters_stack, diff

def calculate_1(data):
    adapters = list(map(int, data.split('\n')))
    _, diff = jolts_difference(adapters)
    counts = Counter(diff)
    return counts[1] * counts[3]


def calculate_2(data):
    adapters = list(map(int, data.split('\n')))

    stack, _ = jolts_difference(adapters)

    @lru_cache(maxsize=256)
    def paths_to_end(i):
        '''Shamelessly taken from https://0xdf.gitlab.io/adventofcode2020/10
        Basically we are checking in the the current index, i
        go from: j :=> [i + 1:i + 4] (or len(stack) for boundary)
        for each index j, recursively call this function if adapter at
        position i and j are compatible (i.e. stack[j] - stack[i] <= 3)
        The sum of this is number of paths from index i. 
        Knowing this count is 1 for the boundary we have our exit condition.
        '''
        if i == len(stack) - 1:
            return 1
        return sum(
            [
                paths_to_end(j)
                for j in range(i + 1, min(i + 4, len(stack)))
                if stack[j] - stack[i] <= 3
            ]
        )

    return paths_to_end(0)
    


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 35
    assert calculate_1(TEST_DATA_2) == 220
    assert calculate_2(TEST_DATA) == 8
    assert calculate_2(TEST_DATA_2) == 19208

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
