import os
from functools import lru_cache


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
    '''Almost a brute-force attempt without optimisations
    Converges after ~80 iterations.
    '''
    layout = [list(row) for row in data.split('\n')]
    sx, sy = len(layout), len(layout[0])
    state = [r[:] for r in layout]
    directions = ['up', 'dn', 'lt', 'rt', 'nw', 'ne', 'sw', 'se']

    if sx > 50:
        print('[Part 2] Hang tight! This will take a little while to converge.')

    @lru_cache
    def coords_in_dirn(dirn, cx, cy):
        if dirn == 'up':
            # going up means to go from x to 0, keeping y same. (in our system)
            xsteps = [cx - i for i in range(1, sx) if cx - i >= 0]
            coords = [(x, cy) for x in xsteps]
        if dirn == 'dn':
            # goin down means to go from x to sx, keeping y same.
            xsteps = [cx + i for i in range(1, sx) if cx + i < sx]
            coords = [(x, cy) for x in xsteps]
        if dirn == 'lt':
            # going left means to go from y to 0. Keeping x same.
            ysteps = [cy - i for i in range(1, sy) if cy - i >= 0]
            coords = [(cx, y) for y in ysteps]
        if dirn == 'rt':
            # going right means to go from y to sy. Keeping x same.
            ysteps = [cy + i for i in range(1, sy) if cy + i < sy]
            coords = [(cx, y) for y in ysteps]
        if dirn == 'nw':
            # going north-west means to decrease x and y together.
            xsteps = [cx - i for i in range(1, sx) if cx - i >= 0]
            ysteps = [cy - i for i in range(1, sy) if cy - i >= 0]
            coords = zip(xsteps, ysteps)
        if dirn == 'ne':
            # going north-east means to decrease x and increase y together.
            xsteps = [cx - i for i in range(1, sx) if cx - i >= 0]
            ysteps = [cy + i for i in range(1, sy) if cy + i < sy]
            coords = zip(xsteps, ysteps)
        if dirn == 'sw':
            # going south-west means to increase x and decrease y together.
            xsteps = [cx + i for i in range(1, sx) if cx + i < sx]
            ysteps = [cy - i for i in range(1, sy) if cy - i >= 0]
            coords = zip(xsteps, ysteps)
        if dirn == 'se':
            # going south-east means to increase x and y together.
            xsteps = [cx + i for i in range(1, sx) if cx + i < sx]
            ysteps = [cy + i for i in range(1, sy) if cy + i < sy]
            coords = zip(xsteps, ysteps)
        yield from coords

    while True:
        next_state = [r[:] for r in state]

        for x in range(sx):
            for y in range(sy):
                curr = state[x][y]
                neighbors = []

                for dirn in directions:
                    for cx, cy in coords_in_dirn(dirn, x, y):
                        if state[cx][cy] == '.':
                            continue
                        neighbors.append(state[cx][cy])
                        break

                if curr == 'L' and neighbors.count('#') == 0:
                    next_state[x][y] = '#'
                elif curr == '#' and neighbors.count('#') >= 5:
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
