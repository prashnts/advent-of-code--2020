from collections import defaultdict


INPUT = '6,3,15,13,1,0'


def calculate_1(data, iters):
    start_nums = list(map(int, data.split(',')))

    seen = defaultdict(list)
    last_spoken = None

    for turn in range(iters):
        if start_nums:
            num = start_nums.pop(0)
            seen[num].append(turn)
            last_spoken = num
            continue

        if len(seen[last_spoken]) == 1:
            seen[0].append(turn)
            last_spoken = 0
            continue

        age = seen[last_spoken][-1] - seen[last_spoken][-2]

        seen[age].append(turn)
        last_spoken = age

    return [k for k, v in seen.items() if turn in v][0]


if __name__ == '__main__':
    assert calculate_1('0,3,6', 2020) == 436
    assert calculate_1('1,3,2', 2020) == 1
    assert calculate_1('2,1,3', 2020) == 10
    assert calculate_1('1,2,3', 2020) == 27
    assert calculate_1('2,3,1', 2020) == 78
    assert calculate_1('3,2,1', 2020) == 438
    assert calculate_1('3,1,2', 2020) == 1836

    # assert calculate_1('0,3,6', 30000000) == 175594
    # assert calculate_1('1,3,2', 30000000) == 2578
    # assert calculate_1('2,1,3', 30000000) == 3544142
    # assert calculate_1('1,2,3', 30000000) == 261214
    # assert calculate_1('2,3,1', 30000000) == 6895259
    # assert calculate_1('3,2,1', 30000000) == 18
    # assert calculate_1('3,1,2', 30000000) == 362

    answer_1 = calculate_1(INPUT, 2020)
    answer_2 = calculate_1(INPUT, 30000000)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
