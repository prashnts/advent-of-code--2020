import os


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc\
'''

def decode_input(data):
    lines = data.split('\n')
    for line in lines:
        policy, password = line.split(': ')
        ranges, character = policy.split(' ')
        a, b = [int(x) for x in ranges.split('-')]
        yield ((a, b, character), password)


def calculate_1(data):
    db = decode_input(data)
    valid_passwords = 0

    for policy, password in db:
        min_, max_, char = policy
        char_count = password.count(char)

        if min_ <= char_count <= max_:
            valid_passwords += 1

    return valid_passwords


def calculate_2(data):
    db = decode_input(data)
    valid_passwords = 0

    for policy, password in db:
        pos_a, pos_b, char = policy

        c1 = password[pos_a - 1]
        c2 = password[pos_b - 1]

        if (c1 == char or c2 == char) and c1 != c2:
            valid_passwords += 1

    return valid_passwords


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 2
    assert calculate_2(TEST_DATA) == 1

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
