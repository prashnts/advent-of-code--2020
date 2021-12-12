import os

from itertools import combinations


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576\
'''

def calculate_1(data, n_preamble):
    nums = list(map(int, data.split('\n')))

    for i in range(n_preamble, len(nums)):
        current = nums[i]
        # Get previous numbers
        prev_nums = nums[i - n_preamble:i]
        # Make combinations of those numbers
        combs = combinations(prev_nums, 2)
        # Take only those that are not equal to each other
        combs_u = filter(lambda x: x[0] != x[1], combs)
        # Sum those numbers
        prev_sums = map(sum, combs_u)

        # check if current is in those sums. if not, we return it.
        if current not in prev_sums:
            return current


def calculate_2(data, n_preamble):
    nums = list(map(int, data.split('\n')))
    offending_num = calculate_1(data, n_preamble)
    subset = nums[:nums.index(offending_num)]

    # We need to look at all the continuous subsets of the numbers' subset.
    # Once we encounter a sum that equals offending number, we're good.
    # I know this can be optimised a lot, but might not be necessary.
    for offset in range(1, len(subset) // 2):
        for i in range(len(subset)):
            cont_nums = subset[i:i + offset]
            if sum(cont_nums) == offending_num:
                return min(cont_nums) + max(cont_nums)

    # If we reach here, we've got a problem.
    raise RuntimeError('Cannot find a valid subset')


if __name__ == '__main__':
    assert calculate_1(TEST_DATA, 5) == 127
    assert calculate_2(TEST_DATA, 5) == 62

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data, 25)
    answer_2 = calculate_2(data, 25)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
