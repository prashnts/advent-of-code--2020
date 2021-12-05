import os
import re
import hashlib


__here__ = os.path.dirname(__file__)

TEST_DATA = '''\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.\
'''

TEST_DATA_2 = '''\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.\
'''


def decode_data(data):
    lines = data.split('\n')

    bags_capacity = {}

    for line in lines:
        main_bag, contents = line.split(' bags contain ')

        for content in contents.split(', '):
            if main_bag not in bags_capacity:
                bags_capacity[main_bag] = {}

            count_s, color_s = content.split(' ', 1)

            if count_s == 'no':
                continue

            count = int(count_s)
            color = re.sub(r'\sbags?\.?', '', color_s)

            bags_capacity[main_bag][color] = count
    return bags_capacity


def parent_chain(node):
    '''Returns list of nodes that are direct parents of the current node.

    It recursively travereses the parents until head node is found.
    '''

    visit_order = []

    def visit_node(n, j):
        visit_order.append(n)
        if n.is_head:
            return
        for i, m in enumerate(n.parents):
            visit_node(m, j + 1)

    visit_node(node, 0)
    return visit_order[1:]  # Skip first one.


# flake8: noqa: C901
def node_factory(ruleset):
    '''Returns a class Node bound to given ruleset.

    The reason for wrapping this class in here is to provide the lookup data.
    The lookup data is used to traverse the graph nature of the data.

    Node is a hashable class, meaning you can perform set operations on it.
    Finally this also provides helpful properties:

    -> Node.children - returns all the immediate child nodes.
    -> Node.is_head - use it to find out if this node does not have any parent nodes.
    -> Node.contents - returns child nodes and their capacities.
    -> Node.parents - returns all the parent nodes of this node.
    '''
    class Node:
        def __init__(self, node_id):
            self.id = node_id

        @property
        def parents(self):
            colors = []
            for color, childs in ruleset.items():
                if self.id in childs:
                    colors.append(Node(color))
            return colors

        @property
        def children(self):
            childs = ruleset[self.id]
            return [Node(c) for c in childs.keys()]

        @property
        def is_head(self):
            return not self.parents

        @property
        def contents(self):
            childs = ruleset[self.id]
            return [(Node(c), v) for c, v in childs.items()]

        def __eq__(self, other):
            return self.id == other.id

        def __hash__(self):
            # Shitty attempt to make this node hashable.
            # So that we can use sets.
            return int(hashlib.md5(self.id.encode()).hexdigest(), 16)

        def __repr__(self):
            return f'<Node {self.id}>'

    return Node


def calculate_1(data):
    ruleset = decode_data(data)
    Node = node_factory(ruleset)

    start = Node('shiny gold')

    return len(set(parent_chain(start)))


def calculate_2(data):
    ruleset = decode_data(data)
    capacities = {bag: sum(contents.values()) for bag, contents in ruleset.items()}
    Node = node_factory(ruleset)

    start = Node('shiny gold')

    def get_bag_capacity(node):
        '''Recursively traverse the node and get the total capacity.'''
        if not node.contents:
            return capacities[node.id]

        count = 0
        for child, capacity in node.contents:
            count += capacity
            count += capacity * get_bag_capacity(child)

        return count

    return get_bag_capacity(start)



if __name__ == '__main__':
    assert calculate_1(TEST_DATA) == 4
    assert calculate_2(TEST_DATA) == 32
    assert calculate_2(TEST_DATA_2) == 126

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answer_1 = calculate_1(data)
    answer_2 = calculate_2(data)

    print(f'{answer_1=}')
    print(f'{answer_2=}')
