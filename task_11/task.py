import os


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL\
'''

def gen_neighbors(array, x, y):
    '''Generated points in NSWE and diagonal directions

    On edges only valid points are generated.
    '''
    dirs = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
    ]

    for x, y in dirs:
        if x >= 0 and y >= 0:
            try:
                yield array[x][y]
            except IndexError:
                continue


def calculate_1(data):
    layout = [list(row) for row in data.split('\n')]
    state = [r[:] for r in layout]

    while True:
        next_state = [r[:] for r in state]

        for x in range(len(state)):
            for y in range(len(state[0])):
                curr = state[x][y]
                neighbors = list(gen_neighbors(state, x, y))

                if curr == 'L' and neighbors.count('#') == 0:
                    next_state[x][y] = '#'
                elif curr == '#' and neighbors.count('#') >= 4:
                    next_state[x][y] = 'L'

        if state == next_state:
            break

        state = next_state

    occupied_seats = sum([row.count('#') for row in state])

    return occupied_seats


def calculate_2(data):
    layout = [list(row) for row in data.split('\n')]
    state = [r[:] for r in layout]

    while True:
        next_state = [r[:] for r in state]

        for x in range(len(state)):
            for y in range(len(state[0])):
                curr = state[x][y]
                neighbors = list(gen_neighbors(state, x, y))

                if curr == 'L' and neighbors.count('#') == 0:
                    next_state[x][y] = '#'
                elif curr == '#' and neighbors.count('#') >= 4:
                    next_state[x][y] = 'L'

        if state == next_state:
            break

        state = next_state

    occupied_seats = sum([row.count('#') for row in state])

    return occupied_seats


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 37
    assert calculate_2(TEST_DATA) == 26

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
