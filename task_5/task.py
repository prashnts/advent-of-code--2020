import os

__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
1721
979
366
299
675
1456\
'''

def split(arr):
    mid = len(arr) // 2
    return arr[:mid], arr[mid:]


def seat_id(path):
    row_space = list(range(128))
    col_space = list(range(8))
    current_row = row_space
    current_col = col_space

    for direction in path[:7]:
        lower, upper = split(current_row)
        if direction == 'F':
            current_row = lower
        elif direction == 'B':
            current_row = upper

    for direction in path[7:]:
        lower, upper = split(current_col)
        if direction == 'L':
            current_col = lower
        elif direction == 'R':
            current_col = upper

    row = current_row[0]
    column = current_col[0]

    return (row * 8) + column


def calculate_1(data):
    paths = data.split('\n')
    seat_ids = [seat_id(path) for path in paths]
    return max(seat_ids)


def calculate_2(data):
    paths = data.split('\n')
    seat_ids = [seat_id(path) for path in paths]

    all_seats = set(range(min(seat_ids), max(seat_ids) + 1))

    remaining_seats = all_seats - set(seat_ids)
    return remaining_seats.pop()


if __name__ == '__main__':
    assert seat_id('FBFBBFFRLR') == 357
    assert seat_id('BFFFBBFRRR') == 567
    assert seat_id('FFFBBBFRRR') == 119
    assert seat_id('BBFFBBFRLL') == 820

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
