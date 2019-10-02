from builder import Board, import_minos
from stack import Point, Tree


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


def test_stack():

    path = [(3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]
    foo = Tree(path)

    # test pushing and popping
    while(foo.curr_branch):
        print(foo.curr_branch.x, ' ', foo.curr_branch.y)
        foo.pop()


def test_tree_paths():
    path = [(3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]
    foo = Tree(path)

    print('most recent path', foo.most_recent_path())

    paths = [[(4, 1), (4, 0), (3, 0), (2, 0)],
            [(2, 1), (2, 2), (2, 3), (3, 3), (3, 4)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4)]
            ]

    for path in paths:
        # ok to put paths as same color because endpoints are used to mark
        # delineation between different paths
        endpoint = Point(path[0][0], path[0][1], 'r', True)
        foo.push(endpoint)
        foo.paths.append(endpoint)

        for i in range(1, len(path) - 1):
            foo.push(Point(path[i][0], path[i][1], 'r'))
            # print(foo.curr_branch.previous)

        i = len(path) - 1
        foo.push(Point(path[i][0], path[i][1], 'r', True))

    paths = foo.all_paths()

    for path in paths:
        print(path)


def test_validate():
    # should return valid
    minos_dict = import_minos()
    foo = Board(5, minos_dict)
    mino = [(3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]

    # want to move away from using temp_game
    # foo.temp_game = [
    # [None, None, None, None, None],
    # [None, None, None, None, None],
    # [None, None, None, None, None],
    # [None, 'rr', 'r', None, None],
    # [None, None, 'r', 'r', 'rr']
    # ]

    foo.tree = Tree(mino)

    print(foo.validate_board())

    # should return invalid, cluster w/ (4,0) and (4,1)
    mino = [(3, 0), (3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]

    foo.tree = Tree(mino)
    print(foo.validate_board())


def test_rollback():
    minos_dict = import_minos()
    foo = Board(5, minos_dict)
    mino = [(3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]

    foo.tree = Tree(mino)

    print("Testing rollback")
    print(foo.rollback())

    print(foo.tree.most_recent_path())
    print(foo.tree.curr_branch)


def test_extend():
    minos_dict = import_minos()
    foo = Board(5, minos_dict)
    mino = [(3, 0), (3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]
    foo.tree = Tree(mino)
    cluster = {(4,1), (4,0)}

    # this will test adding at the 'end' of the line: should add (4,0)
    print(foo.fill_holes(cluster, 'r'))
    print(foo.tree.most_recent_path())
    print(foo.tree.root)
    print(foo.tree.root.next[0])

    # this will test adding at the 'beginning' of the line: should add (4,0)
    foo = Board(5, minos_dict)
    mino = [(4, 4), (4, 3), (4, 2), (3, 2), (3, 1), (3, 0)]
    foo.tree = Tree(mino)
    cluster = {(4,1), (4,0)}
    print(foo.fill_holes(cluster, 'r'))
    print(foo.tree.most_recent_path())
    print(foo.tree.curr_branch)
    print(foo.tree.curr_branch.previous)



test_extend()
