import os


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
abc

a
b
c

ab
ac

a
a
a
a

b\
'''

def decode_input(data):
    lines = data.split('\n')
    accum = []

    for line in lines:
        if line != '':
            accum.append(line)
            continue
        yield accum
        accum = []

    if accum:
        yield accum


def calculate_1(data):
    grouped_answers = decode_input(data)
    yes_count = 0

    for answers in grouped_answers:
        answer = ''.join(answers)
        yes_count += len(set(answer))

    return yes_count


def calculate_2(data):
    grouped_answers = decode_input(data)
    all_yes_count = 0

    for groups in grouped_answers:
        for question in set(''.join(groups)):
            if all([question in group for group in groups]):
                all_yes_count += 1

    return all_yes_count


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 11
    assert calculate_2(TEST_DATA) == 6

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
