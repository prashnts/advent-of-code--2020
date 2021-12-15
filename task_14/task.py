import os
import re

from collections import defaultdict


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0\
'''
TEST_DATA_2 = '''\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1\
'''

def bit_string(number):
    '''Return a padded 36bit representation of number'''
    return bin(number)[2:].zfill(36)


def calculate_1(data):
    mem = defaultdict(int)
    mask = 'X' * 36

    def apply_bitmask(mask, number):
        bits = bit_string(number)
        pairs = zip(mask, bits)
        mapper = lambda x: x[0] if x[0] != 'X' else x[1]
        masked = ''.join(map(mapper, pairs))
        return int(masked, base=2)

    for inst in data.split('\n'):
        if 'mask' in inst:
            mask = inst[7:]
        else:
            pattern = r'mem\[(\d+)\] = (\d+)'
            addr, value = map(int, re.match(pattern, inst).groups())
            masked_val = apply_bitmask(mask, value)
            mem[addr] = masked_val

    return sum(mem.values())


def calculate_2(data):
    mem = defaultdict(int)
    mask = 'X' * 36

    def apply_bitmask(mask, number):
        bits = bit_string(number)
        pairs = zip(mask, bits)
        mapper = lambda x: x[1] if x[0] == '0' else x[0]
        masked = ''.join(map(mapper, pairs))
        domain = masked.count('X')

        # We now have a masked address of format: 00X0X0X
        # We want to replace those Xs with all the combinations
        # of zeros and ones.
        # To do that, we notice that these replacements have
        # to be applied based on bits in numbers in 2^domain. 
        # So, we generate those digits and one by one replace
        # the X with corresponding bit.
        for d in range(2 ** domain):
            overlay = bin(d)[2:].zfill(domain)
            overlaid = masked
            for bit in overlay:
                overlaid = overlaid.replace('X', bit, 1)
            yield overlaid

    for inst in data.split('\n'):
        if 'mask' in inst:
            mask = inst[7:]
        else:
            pattern = r'mem\[(\d+)\] = (\d+)'
            addr, value = map(int, re.match(pattern, inst).groups())
            masked_addrs = apply_bitmask(mask, addr)

            for maddr in masked_addrs:
                mem[maddr] = value

    return sum(mem.values())


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 165
    assert calculate_2(TEST_DATA_2) == 208

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
