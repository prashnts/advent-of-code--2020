import os


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#\
'''

def calculate(data, vstep, hstep):
    lines = data.split('\n')
    x_extent = len(lines[0])

    visited_trees = 0
    vpos = 0
    hpos = 0

    while hpos < len(lines):
        if lines[hpos][vpos] == '#':
            visited_trees += 1
        hpos += hstep
        vpos += vstep
        vpos = vpos % x_extent
    return visited_trees


def calculate_1(data):
    return calculate(data, 3, 1)


def calculate_2(data):
    a1 = calculate(data, 1, 1)
    a2 = calculate(data, 3, 1)
    a3 = calculate(data, 5, 1)
    a4 = calculate(data, 7, 1)
    a5 = calculate(data, 1, 2)
    return a1 * a2 * a3 * a4 * a5


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 7
    assert calculate_2(TEST_DATA) == 336

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
