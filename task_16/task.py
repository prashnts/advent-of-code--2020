import os
import re

from collections import defaultdict


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12\
'''
TEST_DATA_2 = '''\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9\
'''


def decode_input(data):
    lines = data.split('\n')
    ruleset = {}

    while True:
        # Collect "Rules"
        line = lines.pop(0)
        if line == '':
            break
        field, rule = line.split(': ')
        ruleset[field] = rule

    assert lines.pop(0) == 'your ticket:'
    my_ticket = list(map(int, lines.pop(0).split(',')))
    lines.pop(0)     # Don't need this
    assert lines.pop(0) == 'nearby tickets:'

    nearby_tickets = []
    while lines:
        line = lines.pop()
        nearby_tickets.append(list(map(int, line.split(','))))

    return ruleset, my_ticket, nearby_tickets


def matches_rule(rule, x):
    pattern = r'(\d+)-(\d+) or (\d+)-(\d+)'
    a, b, c, d = map(int, re.match(pattern, rule).groups())
    return a <= x <= b or c <= x <= d


def calculate_1(data):
    ruleset, my_ticket, nearby_tickets = decode_input(data)

    error_rate = 0
    for ticket in nearby_tickets:
        for value in ticket:
            if not any([matches_rule(rule, value) for rule in ruleset.values()]):
                error_rate += value

    return error_rate


def calculate_2(data):
    ruleset, my_ticket, nearby_tickets = decode_input(data)

    valid_tickets = []

    for ticket in nearby_tickets:
        valid = all([
            any([
                matches_rule(rule, value)
                for rule in ruleset.values()
            ])
            for value in ticket
        ])

        if valid:
            valid_tickets.append(ticket)

    # Now we need to find which field is which.
    # Basically the each rule on each ticket's corresponding field
    # needs to be _all_ matching. We use that fact.
    columns = list(zip(*valid_tickets))
    rule_ix = defaultdict(set)

    # Build candidate rules.
    for ix, col in enumerate(columns):
        for rulename, rule in ruleset.items():
            if all([matches_rule(rule, x) for x in col]):
                rule_ix[ix].add(rulename)

    all_are_one = lambda x: all([len(v) == 1 for v in x.values()])

    # Set operations to isolate single field values:
    while not all_are_one(rule_ix):
        for k, v in rule_ix.items():
            if len(v) == 1:
                # Update all the others by subtracting this field
                # to their field.
                for k2 in rule_ix:
                    if k2 != k:
                        rule_ix[k2] = rule_ix[k2] - v


    rule_mapping = {}
    for k, v in rule_ix.items():
        rule_mapping[k] = v.pop()

    my_ticket_mapped = {}
    for i, val in enumerate(my_ticket):
        my_ticket_mapped[rule_mapping[i]] = val

    answer = 1
    for field, value in my_ticket_mapped.items():
        if field.startswith('departure'):
            answer *= value

    return answer



if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 71
    assert calculate_2(TEST_DATA_2) == 1

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
