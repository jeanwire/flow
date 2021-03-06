import os
import json
import random
import re
import copy
import stack


def main():
    minos_dict = import_minos()

    starter_board = Board(5, minos_dict)

    print(starter_board)

    # when board is completed, write to file in json format


class Board(object):
    def __init__(self, size, minos_dict):
        self.size = size
        self.game = [[None for _ in range(size)] for _ in range(size)]
        # just here until tree is fully integrated into builder
        self.temp_game = [[None for _ in range(size)] for _ in range(size)]
        self.complete = False
        self.unused_colors = ['m', 'p', 'c', 'o', 'y', 'b', 'g', 'r']
        # just here until adding the mino is changed to be stack-centric
        self.paths = []
        edges = [(0, i) for i in range(1, size - 1)]
        edges.extend([(i, 0) for i in range(1, size - 1)])
        edges.extend([(i, size - 1) for i in range(1, size - 1)])
        edges.extend([(size - 1, i) for i in range(1, size - 1)])
        self.edges = set(edges)
        self.corners = set([(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)])
        self.extremities = self.edges.union(self.corners)
        self.tree = stack.Tree()

        inserted = False
        while not inserted:
            mino = copy.deepcopy(select_mino(minos_dict))

            if (len(mino[0]) <= self.size):
                inserted = self.insert(mino)

        # for i in range(0,5):
        #     self.draw_line()
            # self.validate_line()
            # valid = self.validate_board()
            # if not isinstance(valid, set)


    def __str__(self):
        return "\n".join([" ".join(str(item) for item in row) for row in self.game])


    def insert(self, mino):
        row = random.randint(0, self.size - len(mino))
        col = random.randint(0, self.size - len(mino[0]))

        color = self.unused_colors.pop()
        valid = self.mino_in_board(mino, row, col, color)
        # if mino was placed in invalid spot, attempt to place it again
        if (isinstance(valid, set) and row + 1 < self.size - len(mino)):
            valid = self.mino_in_board(mino, row + 1, col, color)
        elif (isinstance(valid, set) and col + 1 < self.size - len(mino[0])):
            valid = self.mino_in_board(mino, row, col + 1, color)
        elif (isinstance(valid, set) and row - 1 >= 0):
            valid = self.mino_in_board(mino, row - 1, col, color)
        elif (isinstance(valid, set) and col - 1 >= 0):
            valid = self.mino_in_board(mino, row, col - 1, color)

        if not isinstance(valid, set):
            return True
        self.game = [[None for _ in range(self.size)] for _ in range(self.size)]
        return False


    def mino_in_board(self, mino, row, col, color):
        temp_visited = set()
        endpoints = set()

        mino_row = 0
        for i in range(row, row + len(mino)):
            mino_col = 0
            for j in range(col, col + len(mino[0])):
                if (mino[mino_row][mino_col] != 'O'):
                    if (len(mino[mino_row][mino_col]) == 2):
                        endpoints.add((i, j))
                    else:
                        temp_visited.add((i, j))
                mino_col += 1
            mino_row += 1

        valid = self.validate_board()

        if (not isinstance(valid, set)):
            path = self.mino_to_line(temp_visited, endpoints)
            print('path: ', path)
            self.tree.push(stack.Point(path[0][0], path[0][1], 'r', True))
            self.game[path[0][0]][path[0][1]] = 'rr'
            for i in range(1, len(path) - 1):
                self.tree.push(stack.Point(path[i][0], path[i][1], 'r'))
                self.game[path[i][0]][path[i][1]] = 'r'
            self.tree.push(stack.Point(path[-1][0], path[-1][1], 'r', True))
            self.game[path[-1][0]][path[-1][1]] = 'rr'
        return valid


    def mino_to_line(self, mino_sqs, endpts):
        path = [None for i in range(len(mino_sqs) + 2)]
        path[0] = endpts.pop()
        path[len(path) - 1] = endpts.pop()
        for i in range(0, len(mino_sqs)):
            pot_next_point = set()
            pot_next_point.add((path[i][0] - 1, path[i][1]))
            pot_next_point.add((path[i][0] + 1, path[i][1]))
            pot_next_point.add((path[i][0], path[i][1] - 1))
            pot_next_point.add((path[i][0], path[i][1] + 1))
            next_point = pot_next_point.intersection(mino_sqs)
            mino_sqs = mino_sqs.difference(next_point)
            path[i + 1] = next_point.pop()

        return path


    def draw_line(self):
        self.temp_game = copy.deepcopy(self.game)
        board = self.temp_game
        color = self.unused_colors.pop()
        path = []

        pot_endpoints = self.find_pot_ends()

        if pot_endpoints:
            curr_point = pot_endpoints.pop()
        else:
            print(self)
            # for debugging: will print the board then crash
            curr_point = pot_endpoints.pop()
        point = Point(curr_point[0], curr_point[1], color, True)
        tree.push(point)
        board[curr_point[0]][curr_point[1]] = color + color
        # if the endpoint is on the edge, it has a 1/4 chance of moving along the edge
        if curr_point in self.extremities:
            if random.random() < 0.25:
                self.edge(path, color)
            else:
                self.onion(path, color)
        else:
            self.onion(path, color)

        if len(tree.visited_sqs()) == self.size * self.size:
            self.complete = True


    def edge(self, path, color):
        curr_point = path[0]
        horizontal = True
        vertical = False
        side = horizontal
        direction = 0
        board = self.temp_game

        neighbors = self.ortho_neighbors(curr_point)
        for neighbor in neighbors:
            if neighbor in self.extremities:
                if (neighbor[0] < curr_point[0]):
                    side = horizontal
                    direction = -1
                elif (neighbor[0] > curr_point[0]):
                    side = horizontal
                    direction = +1
                elif (neighbor[1] < curr_point[1]):
                    side = vertical
                    direction = -1
                else:
                    side = vertical
                    direction = +1

                curr_point = neighbor
                point = Point(curr_point[0], curr_point[1], color)
                tree.push(point)
                board[curr_point[0]][curr_point[1]] = color
                break

        while (len(path) < 3 or random.randint(0, 9 - len(path))):
            # if the line can keep going in the same direction
            if side == horizontal and (curr_point[0], curr_point[1] + direction) in self.extremities:
                if not board[curr_point[0]][curr_point[1] + direction]:
                    curr_point = (curr_point[0], curr_point[1] + direction)
                    point = Point(curr_point[0], curr_point[1], color)
                    tree.push(point)
                    board[curr_point[0]][curr_point[1]] = color
                else:
                    break
            elif side == vertical and (curr_point[0] + direction, curr_point[1]) in self.extremities:
                if not board[curr_point[0] + direction][curr_point[1]]:
                    curr_point = (curr_point[0] + direction, curr_point[1])
                    point = Point(curr_point[0], curr_point[1], color)
                    tree.push(point)
                    board[curr_point[0]][curr_point[1]] = color
                else:
                    break
            # if the line needs to turn
            else:
                if side == horizontal:
                    # direction is now vertical
                    side = not side
                    if (curr_point[0] + direction, curr_point[1]) in self.extremities:
                        if not board[curr_point[0] + direction][curr_point[1]]:
                            curr_point = (curr_point[0] + direction, curr_point[1])
                            point = Point(curr_point[0], curr_point[1], color)
                            tree.push(point)
                            board[curr_point[0]][curr_point[1]] = color
                        else:
                            break
                    elif (curr_point[0] - direction, curr_point[1]) in self.extremities:
                        if not board[curr_point[0] - direction][curr_point[1]]:
                            direction = - direction
                            curr_point = (curr_point[0] + direction, curr_point[1])
                            point = Point(curr_point[0], curr_point[1], color)
                            tree.push(point)
                            board[curr_point[0]][curr_point[1]] = color
                        else:
                            break
                    else:
                        break
                else:
                    side = not side
                    if (curr_point[0], curr_point[1] + direction) in self.extremities:
                        if not board[curr_point[0]][curr_point[1] + direction]:
                            curr_point = (curr_point[0], curr_point[1] + direction)
                            point = Point(curr_point[0], curr_point[1], color)
                            tree.push(point)
                            board[curr_point[0]][curr_point[1]] = color
                        else:
                            break
                    elif (curr_point[0], curr_point[1] - direction) in self.extremities:
                        if not board[curr_point[0]][curr_point[1] - direction]:
                            direction = - direction
                            curr_point = (curr_point[0], curr_point[1] + direction)
                            point = Point(curr_point[0], curr_point[1], color)
                            tree.push(point)
                            board[curr_point[0]][curr_point[1]] = color
                        else:
                            break
                    else:
                        break

        self.tree.curr_branch.end = True
        board[curr_point[0]][curr_point[1]] *= 2
        self.validate_line(path, color)


    def onion(self, path, color):
        """Draws a line that traces along the lines already present in the board.
        The line may trace along the edges if it cannot trace any further along
        the already present lines."""
        curr_point = path[0]
        board = self.temp_game
        # randomly ends after path is 3 sqs long and <= 9 sqs long
        # while (len(path) < 3 or random.randint(0, 9 - len(path))):
        while (len(path) < random.randint(3, max(3, 9 - len(path)))):
            empty_neighbors = self.ortho_neighbors(curr_point)
            # if there is only one neighbor, need to make sure line isn't doubling back
            if len(empty_neighbors) == 1:
                point = empty_neighbors.pop()
                if len(self.filled_neighbors(point, path)[1]) < 3:
                    curr_point = point
                    point_P = Point(curr_point[0], curr_point[1], color)
                    tree.push(point_P)
                    board[curr_point[0]][curr_point[1]] = color
                else:
                    break
            # if there are multiple neighbors, need to determine which one
            # allows for "onion" behavior, which is a sq that contains filled neighbors
            elif empty_neighbors:
                for neighbor in empty_neighbors:
                    if self.filled_neighbors(neighbor, path)[0]:
                        curr_point = neighbor
                        point_P = Point(curr_point[0], curr_point[1], color)
                        tree.push(point_P)
                        board[curr_point[0]][curr_point[1]] = color
                        break
            # if there are no neighbors, line must end
            else:
                break

        self.tree.curr_branch.end = True
        board[curr_point[0]][curr_point[1]] = color + color
        self.validate_line(path, color)
        return board


    def validate_line(self, path, color):
        # if line is only 2 sqs long, need to extend
        board = self.temp_game
        if len(path) < 3:
            self.extend_path(path, color)

        valid = self.validate_board(path)

        needs_rollback = False
        # if line has left 1 or 2 sqs open adjacent to the endpoint, need to extend the line
        # if open sqs are not adjacent to an endpoint, need to remove sqs from the path
        while isinstance(valid, set):
            hole_filled = self.fill_holes(path, valid, color)
            if not hole_filled:
                needs_rollback = True
                break
            valid = self.validate_board(path)

        while (needs_rollback and len(path) > 3):
            self.rollback(path)
            valid = self.validate_board(path)
            if not isinstance(valid, set):
                needs_rollback = False

        # adding the line as it was randomly drawn may not be possible
        if (not needs_rollback and len(path) > 3):
            self.paths.append(path)
            self.game = copy.deepcopy(self.temp_game)
        else:
            self.unused_colors.append(color)


    def validate_board(self):
        """Determines whether a board contains any isolated groups of fewer
        than 3 squares. Returns true or a set of 1 or 2 isolated squares"""
        clusters = []

        visited_sqs = self.tree.visited_sqs()
        checked = visited_sqs.copy()

        first_sq = None

        while(len(checked) < self.size * self.size):
            # need to do this in one loop so we can break out of it
            for i in range(self.size * self.size):
                if (i // 5, i % 5) not in checked:
                    first_sq = (i // 5, i % 5)
                    break;

            cluster = set({first_sq})
            self.bfs(cluster.copy(), cluster, visited_sqs)
            if cluster:
                clusters.append(cluster)
                for sq in cluster:
                    checked.add(sq)
            # reset this value
            first_sq = None

        for cluster in clusters:
            if len(cluster) <= 2:
                return cluster

        return True

    def bfs(self, sqs, cluster, visited_sqs):
        children = set()
        for sq in sqs:
            if (sq[0] != 0 and (sq[0] - 1, sq[1]) not in visited_sqs):
                if (sq[0] - 1, sq[1]) not in cluster:
                    children.add((sq[0] - 1, sq[1]))
                    cluster.add((sq[0] - 1, sq[1]))
            if (sq[0] != self.size - 1 and (sq[0] + 1, sq[1]) not in visited_sqs):
                if (sq[0] + 1, sq[1]) not in cluster:
                    children.add((sq[0] + 1, sq[1]))
                    cluster.add((sq[0] + 1, sq[1]))
            if (sq[1] != 0 and (sq[0], sq[1] - 1) not in visited_sqs):
                if (sq[0], sq[1] - 1) not in cluster:
                    children.add((sq[0], sq[1] - 1))
                    cluster.add((sq[0], sq[1] - 1))
            if (sq[1] != self.size - 1 and (sq[0], sq[1] + 1) not in visited_sqs):
                if (sq[0], sq[1] + 1) not in cluster:
                    children.add((sq[0], sq[1] + 1))
                    cluster.add((sq[0], sq[1] + 1))

        if (len(children)):
            self.bfs(children, cluster, visited_sqs)


    def ortho_neighbors(self, point):
        """Finds the empty neighbors that are orthogonal to the present square"""
        visited = self.tree.visited_sqs()
        neighbors = set()
        if point[0] != 0:
            if not (point[0] - 1, point[1]) in visited:
                neighbors.add((point[0] - 1, point[1]))
        if (point[0] != self.size - 1):
            if not (point[0] + 1, point[1]) in visited:
                neighbors.add((point[0] + 1, point[1]))
        if (point[1] != 0):
            if not (point[0], point[1] - 1) in visited:
                neighbors.add((point[0], point[1] - 1))
        if (point[1] != self.size - 1):
            if not (point[0], point[1] + 1) in visited:
                neighbors.add((point[0], point[1] + 1))

        return neighbors

    def filled_neighbors(self, point):
        """Finds the filled neighbors of the square, including orthogonal and
        diagonal neighbors. Counts the neighbors within the line passed as an
        argument separately from the other neighbors, which is used to prevent
        the lines doubling back upon themselves"""
        board = self.temp_game
        path_list = self.tree.most_recent_path()
        # searching in set is much faster than in list
        path = set()
        for sq in path_list:
            path.add(sq)
        filled_neighbors = []
        own_neighbors = []
        # row above
        if point[0] != 0:
            if board[point[0] - 1][point[1]]:
                if (point[0] - 1,point[1]) not in path:
                    filled_neighbors.append((point[0] - 1,point[1]))
                else:
                    own_neighbors.append((point[0] - 1,point[1]))
            if point[1] != 0 and board[point[0] - 1][point[1] - 1]:
                if (point[0] - 1,point[1] - 1) not in path:
                    filled_neighbors.append((point[0] - 1,point[1] - 1))
                else:
                    own_neighbors.append((point[0] - 1,point[1] - 1))
            if point[1] != self.size - 1 and board[point[0] - 1][point[1] + 1]:
                if (point[0] - 1,point[1] + 1) not in path:
                    filled_neighbors.append((point[0] - 1,point[1] + 1))
                else:
                    own_neighbors.append((point[0] - 1,point[1] + 1))
        # row below
        if point[0] != self.size - 1:
            if board[point[0] + 1][point[1]]:
                if (point[0] + 1,point[1]) not in path:
                    filled_neighbors.append((point[0] + 1,point[1]))
                else:
                    own_neighbors.append((point[0] + 1,point[1]))
            if point[1] != 0 and board[point[0] + 1][point[1] - 1]:
                if (point[0] + 1,point[1] - 1) not in path:
                    filled_neighbors.append((point[0] + 1,point[1] - 1))
                else:
                    own_neighbors.append((point[0] + 1,point[1] - 1))
            if point[1] != self.size - 1 and board[point[0] + 1][point[1] + 1]:
                if (point[0] + 1,point[1] + 1) not in path:
                    filled_neighbors.append((point[0] + 1,point[1] + 1))
                else:
                    own_neighbors.append((point[0] + 1,point[1] + 1))
        # left sq
        if point[1] != 0 and board[point[0]][point[1] - 1]:
            if (point[0],point[1] - 1) not in path:
                filled_neighbors.append((point[0],point[1] - 1))
            else:
                own_neighbors.append((point[0],point[1] - 1))
        # right sq
        if point[1] != self.size - 1 and board[point[0]][point[1] + 1]:
            if (point[0],point[1] + 1) not in path:
                filled_neighbors.append((point[0],point[1] + 1))
            else:
                own_neighbors.append((point[0],point[1] + 1))

        return (filled_neighbors, own_neighbors)


    def rollback(self):
        self.tree.pop()
        point = stack.Point(self.tree.curr_branch.x, self.tree.curr_branch.y, self.tree.curr_branch.color, True)
        self.tree.pop()
        return self.tree.push(point)


    def find_pot_ends(self):
        """Builds up a set of empty squares on the board that either only have 1
        neighbor or are neighbors of the current endpoints"""
        one_neighbor = set()
        endpoints = set()
        line_neighbor = set()

        visited_sqs = self.tree.visited_sqs()

        for i in range(self.size):
            for j in range(self.size):
                if not (i, j) in visited_sqs:
                    neighbors = self.ortho_neighbors((i, j))
                    if len(neighbors) == 1:
                        one_neighbor.add((i, j))
                    elif (i, j) not in self.corners and len(neighbors) == 2:
                        line_neighbor.add((i, j))
                    elif (i, j) not in self.edges and len(neighbors) == 3:
                        line_neighbor.add((i, j))
                # how to determine if sq is endpoint?
                elif len(self.temp_game[i][j]) == 2:
                    endpoints.add((i, j))

        pot_endpoints = one_neighbor.copy()
        for endpoint in endpoints:
            pot_endpoints = pot_endpoints.union(self.ortho_neighbors(endpoint))

        if pot_endpoints:
            return pot_endpoints
        else:
            return line_neighbor


    def extend_path(self, color):
        """Randomly extends a path in any valid direction"""
        path = self.tree.most_recent_path()

        empty_neighbors = self.ortho_neighbors(path[0])
        # if the path can be extended at its beginning
        if empty_neighbors:
            point = stack.Point(self.tree.curr_branch.x, self.tree.curr_branch.y, color)
            self.tree.pop()
            # TODO: what if this isn't push-able?
            self.tree.push(point)
            sq = empty_neighbors.pop()
            point = stack.Point(sq[0], sq[1], color, True)
            return self.tree.push(point)
        # if the path can be extended at its end
        else:
            empty_neighbors = self.ortho_neighbors(path[-1])
            if empty_neighbors:
                sq = empty_neighbors.pop()
                point = stack.Point(sq[0], sq[1], color, True)
                return self.tree.push_start_of_line(point)


    def fill_holes(self, cluster, color):
        """Attempts to fill the holes created by drawing the most recent line"""
        path = self.tree.most_recent_path()
        # seeing if cluster is neighbor to beginning or end of line
        # beginning and end are flipped relative to when they were added
        beginning_neighbors = self.ortho_neighbors(path[0])
        end_neighbors = self.ortho_neighbors(path[len(path) - 1])
        # overlap can only be 1 or 0 squares
        beginning_overlap = cluster.intersection(beginning_neighbors)
        end_overlap = cluster.intersection(end_neighbors)
        if beginning_overlap:
            sq = beginning_overlap.pop()
            pushed = self.tree.push(stack.Point(sq[0], sq[1], color, True))
            if pushed:
                self.tree.curr_branch.previous.end = False
                return pushed
        if end_overlap:
            sq = end_overlap.pop()
            pushed = self.tree.push_start_of_line(stack.Point(sq[0], sq[1], color, True))
            return pushed
        return False


def import_minos():
    with open('minos.json') as minos_file:
        json_data = json.load(minos_file)
        return json_data


def select_mino(minos_dict):
    mino_size = random.randint(3, 6)
    minos = minos_dict[str(mino_size)]
    mino = minos[random.randint(0, len(minos) - 1)]
    return mino


if __name__ == '__main__':
    main()
