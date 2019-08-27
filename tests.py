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


test_edge()
