import os
import math


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
F10
N3
F7
R90
F11\
'''

def decode_input(data):
    lines = data.split('\n')
    for line in lines:
        yield line[0], int(line[1:])


class PositionVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'<Vec x={self.x} y={self.y}>'

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return PositionVector(x, y)

    def __mul__(self, constant):
        x = self.x * constant
        y = self.y * constant
        return PositionVector(x, y)

    def rot(self, amount):
        theta = math.radians(amount)

        px, py = self.x, self.y

        qx = math.cos(theta) * px - math.sin(theta) * py
        qy = math.sin(theta) * px + math.cos(theta) * py
        return PositionVector(int(round(qx)), int(round(qy)))

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


rot_offset = {
    0: PositionVector(1, 0),
    90: PositionVector(0, -1),
    180: PositionVector(-1, 0),
    270: PositionVector(0, 1),
}
dir_offset = {
    'N': PositionVector(0, 1),
    'S': PositionVector(0, -1),
    'E': PositionVector(1, 0),
    'W': PositionVector(-1, 0),
}

def calculate_1(data):
    '''
              N (y)
              │   #
              │ .
        W─────┼───>──E (x)
              │
              │
              S
    '''

    instructions = decode_input(data)
    ship = PositionVector(0, 0)
    direction = 0

    for inst, amnt in instructions:
        if inst == 'F':
            ship += rot_offset[direction] * amnt
        if inst in ['N', 'S', 'E', 'W']:
            ship += dir_offset[inst] * amnt
        if inst == 'R':
            direction += amnt
            direction %= 360
        if inst == 'L':
            direction -= amnt
            direction %= 360

    return ship.manhattan_distance


def calculate_2(data):
    instructions = decode_input(data)
    ship = PositionVector(0, 0)
    waypoint = PositionVector(10, 1)

    for inst, amnt in instructions:
        if inst == 'F':
            # Moves the ship to the waypoint amt times
            ship += waypoint * amnt
        if inst in ['N', 'S', 'E', 'W']:
            waypoint += dir_offset[inst] * amnt
        if inst == 'R':
            waypoint = waypoint.rot(-amnt)
        if inst == 'L':
            waypoint = waypoint.rot(amnt)

    return ship.manhattan_distance


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 25
    assert calculate_2(TEST_DATA) == 286

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
