import os
import re


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in\
'''

TEST_DATA_INVALID = '''\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007\
'''

TEST_DATA_VALID = '''\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719\
'''


def decode_input(data):
    lines = data.split('\n')
    accum = []

    def parse_passport(passport):
        # Takes a list of lines for a passport and returns a dictionary
        fields = ' '.join(passport).split(' ')
        return dict([field.split(':') for field in fields])

    for line in lines:
        if line != '':
            accum.append(line)
            continue
        # whenever we have an empty line we flush the data in accum.
        yield parse_passport(accum)
        accum = []

    if accum:
        # We will have last line which wont be empty.
        yield parse_passport(accum)


def passport_has_all_fields(passport):
    return all([
        'byr' in passport,
        'iyr' in passport,
        'eyr' in passport,
        'hgt' in passport,
        'hcl' in passport,
        'ecl' in passport,
        'pid' in passport,
    ])


def is_valid_passport(passport):
    byr = passport['byr']
    byr_valid = len(byr) == 4 and 1920 <= int(byr) <= 2002

    iyr = passport['iyr']
    iyr_valid = len(iyr) == 4 and 2010 <= int(iyr) <= 2020

    eyr = passport['eyr']
    eyr_valid = len(eyr) == 4 and 2020 <= int(eyr) <= 2030

    hgt = passport['hgt']
    hgt_valid = False
    if hgt.endswith('in'):
        hgt_valid = 59 <= int(hgt.rstrip('in')) <= 76
    elif hgt.endswith('cm'):
        hgt_valid = 150 <= int(hgt.rstrip('cm')) <= 193

    hcl = passport['hcl']
    hcl_valid = re.match(r'#[\da-f]{6}$', hcl, re.I) is not None

    ecl = passport['ecl']
    ecl_valid = ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    pid = passport['pid']
    pid_valid = len(pid) == 9 and re.match(r'\d+', pid)

    return all([
        byr_valid,
        iyr_valid,
        eyr_valid,
        hgt_valid,
        hcl_valid,
        ecl_valid,
        pid_valid,
    ])


def calculate_1(data):
    passports = decode_input(data)
    return len([p for p in passports if passport_has_all_fields(p)])


def calculate_2(data):
    passports = decode_input(data)
    validate = lambda p: passport_has_all_fields(p) and is_valid_passport(p)
    return len([p for p in passports if validate(p)])


if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 2
    assert calculate_2(TEST_DATA_INVALID) == 0
    assert calculate_2(TEST_DATA_VALID) == 4

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
