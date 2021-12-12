import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6\
'''


def decode_input(data):
    lines = data.split('\n')
    for line in lines:
        opcode, argument = line.split(' ')
        yield opcode, int(argument)


def calculate_1(data):
    instructions = list(decode_input(data))
    icounter = 0
    accum = 0
    visited = []

    while True:
        opcode, argument = instructions[icounter]

        if icounter in visited:
            return accum

        visited.append(icounter)

        if opcode == 'nop':
            icounter += 1
        elif opcode == 'acc':
            accum += argument
            icounter += 1
        elif opcode == 'jmp':
            icounter += argument


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 5
    # assert calculate_2(TEST_DATA) == 8

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    # answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    # print(f'{answer_2=}')
