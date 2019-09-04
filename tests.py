from builder import Board


def test_extend():
    foo = Board(5)


    foo.game = [
    [None, None, None, None, None],
    [None, None, None, None, None],
    ['g', 'g', 'g', 'gg', None],
    ['gg', 'rr', 'r', None, None],
    [None, None, 'r', 'r', 'rr']
    ]

    visited = {(2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2),
    (4, 2), (4, 3), (4, 4)}

    path = [(3, 0), (2, 0), (2, 1), (2, 2), (2, 3)]


    for row in foo.game:
        print(row)

    print(path)
    print(" ")

    foo.extend_path(foo.game, path, 'g')

    for row in foo.game:
        print(row)
    print(path)
    print(" ")

    foo.extend_path(foo.game, path, 'g')

    for row in foo.game:
        print(row)
    print(path)

def test_edge():
    foo = Board(5)

    foo.game = [
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, 'rr', 'r', None, None],
    [None, 'gg', 'r', 'r', 'rr']
    ]

    foo.paths = [[(3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]]

    path = [(4, 1)]
    foo.edge(path, foo.game, 'g')
    print(" ")
    for row in foo.game:
        print(row)
    print(path)

    foo1 = Board(5)
    foo1.game = [
    [None, None, None, None, None],
    [None, None, None, None, None],
    ['gg', 'rr', None, None, None],
    [None, 'r', 'r', 'r', 'rr'],
    [None, None, None, None, None]
    ]

    foo1.paths = [[(2, 1), (3, 1), (3, 2), (3, 3), (3, 4)]]
    path = [(2, 0)]
    foo1.edge(path, foo1.game, 'g')
    print(" ")
    for row in foo1.game:
        print(row)
    print(path)

    foo2 = Board(5)
    foo2.game = [
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, 'rr', None, None, None],
    [None, 'r', 'r', 'r', 'rr'],
    [None, None, None, None, 'gg']
    ]

    foo2.paths = [[(2, 1), (3, 1), (3, 2), (3, 3), (3, 4)]]
    path = [(4, 4)]
    foo2.edge(path, foo2.game, 'g')
    print(" ")
    for row in foo2.game:
        print(row)
    print(path)

    foo3 = Board(5)
    foo3.game = [
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, 'rr', None, None, 'gg'],
    [None, 'r', 'r', 'r', 'rr'],
    [None, None, None, None, None]
    ]

    foo3.paths = [[(2, 1), (3, 1), (3, 2), (3, 3), (3, 4)]]
    path = [(2, 4)]
    foo3.edge(path, foo3.game, 'g')
    print(" ")
    for row in foo3.game:
        print(row)
    print(path)

    foo4 = Board(5)
    foo4.game = [
    [None, 'rr', 'gg', None, None],
    [None, 'r', 'r', 'r', 'rr'],
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, None, None, None]
    ]

    foo4.paths = [[(0, 1), (2, 1), (2, 2), (2, 3), (2, 4)]]
    path = [(0, 2)]
    foo4.edge(path, foo4.game, 'g')
    print(" ")
    for row in foo4.game:
        print(row)
    print(path)


def test_fill():
    foo = Board(5)

    foo.game = [
    [None, None, None, None, None],
    [None, None, None, None, None],
    ['g', 'g', 'g', 'gg', None],
    ['gg', 'rr', 'r', None, None],
    [None, None, 'r', 'r', 'rr']
    ]

    path = [(3, 0), (2, 0), (2, 1), (2, 2), (2, 3)]
    cluster = set([(4, 0), (4, 1)])

    hole_filled = foo.fill_holes(foo.game, path, cluster, 'g')
    print(hole_filled)
    print(" ")

    for line in foo.game:
        print(line)

    print(' ')
    print(path)


test_fill()
