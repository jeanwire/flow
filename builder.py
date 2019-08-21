import os
import json
import random
import re
import copy


def main():
    minos_dict = import_minos()
    board = Board(5)
    inserted = False
    while (not inserted):
        mino = copy.deepcopy(select_mino(minos_dict))
        print(mino)

        if (len(mino[0]) <= board.size):
            temp_board, inserted = board.insert(mino)

    board.game = copy.deepcopy(temp_board)
    for line in board.game:
        print(line)

    print(" ")

    board.draw_line()
    for line in board.game:
        print(line)

    print(" ")

    board.draw_line()
    for line in board.game:
        print(line)

    # build lines around mino(s)
    # validate board, repeat adding lines if necessary
    # when board is completed, write to file in json format


class Board(object):
    def __init__(self, size):
        self.size = size
        self.game = []
        for i in range(size):
            self.game.append([None] * size)
        self.paths = []
        self.complete = False
        self.unused_colors = ['m', 'p', 'c', 'o', 'y', 'b', 'g', 'r']


    def insert(self, mino):
        row = random.randint(0, self.size - len(mino))
        col = random.randint(0, self.size - len(mino[0]))

        color = self.unused_colors.pop()
        temp, valid = self.mino_in_board(mino, row, col, color)


        if (isinstance(valid, set) and row + 1 < self.size - len(mino)):
            temp, valid = self.mino_in_board(mino, row + 1, col, color)
        elif (isinstance(valid, set) and col + 1 < self.size - len(mino[0])):
            temp, valid = self.mino_in_board(mino, row, col + 1, color)
        elif (isinstance(valid, set) and row - 1 >= 0):
            temp, valid = self.mino_in_board(mino, row - 1, col, color)
        elif (isinstance(valid, set) and col - 1 >= 0):
            temp, valid = self.mino_in_board(mino, row, col - 1, color)
        return (temp, valid)


    def mino_in_board(self, mino, row, col, color):
        temp = copy.deepcopy(self.game)
        temp_visited = set()
        endpoints = set()

        mino_row = 0
        for i in range(row, row + len(mino)):
            mino_col = 0
            for j in range(col, col + len(mino[0])):
                if (mino[mino_row][mino_col] != 'O'):
                    temp[i][j] = re.sub('X', color, mino[mino_row][mino_col])
                    if (len(mino[mino_row][mino_col]) == 2):
                        endpoints.add((i, j))
                    else:
                        temp_visited.add((i, j))
                mino_col += 1
            mino_row += 1

        valid = self.validate_board(temp, temp_visited.union(endpoints))

        if (not isinstance(valid, set)):
            path = self.mino_to_line(temp_visited, endpoints)
            print(path)
            self.paths.append(path)
        return (temp, valid)


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
        board = copy.deepcopy(self.game)
        color = self.unused_colors.pop()
        path = []

        pot_endpoints = self.find_pot_ends(board)

        curr_point = pot_endpoints.pop()
        path.append(curr_point)
        board[curr_point[0]][curr_point[1]] = color + color
        # if the endpoint is on the edge, it can move along the edge
        self.game = self.onion(path, board, color)
        # self.game = self.edge(path, board, color, curr_point)
        total_sqs_filled = 0
        for path in self.paths:
            total_sqs_filled += len(path)
        if total_sqs_filled == self.size * self.size:
            self.complete = True


    def onion(self, path, board, color):
        """Draws a line that traces along the lines already present in the board.
        The line may trace along the edges if it cannot trace any further along
        the already present lines."""
        curr_point = path[0]
        # randomly ends after path is 3 sqs long and <= 8 sqs long
        while (len(path) < 3 or random.randint(0, 8 - len(path))):
            empty_neighbors = self.ortho_neighbors(curr_point, board)
            # if there is only one neighbor, don't need to perform any further analysis
            if len(empty_neighbors) == 1:
                curr_point = empty_neighbors.pop()
                path.append(curr_point)
                board[curr_point[0]][curr_point[1]] = color
            # if there are multiple neighbors, need to determine which one
            # allows for "onion" behavior
            elif empty_neighbors:
                for neighbor in empty_neighbors:
                    if self.filled_neighbors(neighbor, board, path)[0]:
                        curr_point = neighbor
                        path.append(curr_point)
                        board[curr_point[0]][curr_point[1]] = color
                        break;
            # if there are no neighbors, line must end
            else:
                break

        board[curr_point[0]][curr_point[1]] = color + color

        print(" ")
        for line in board:
            print(line)

        # if line is only 2 sqs long, need to extend in other direction
        if len(path) < 3:
            self.extend_path(board, path, color)

        valid = self.validate_board(board, path)

        needs_rollback = False
        # if line has left 1 or 2 sqs open adjacent to the endpoint, need to extend the line
        # if open sqs are not adjacent to an endpoint, need to remove sqs from the path
        while isinstance(valid, set):
            self.extend_path(board, path, color)
            prev_valid = valid
            valid = self.validate_board(board, path)
            if prev_valid == valid:
                needs_rollback = True
                break

        while (needs_rollback and len(path) > 3):
            self.rollback(board, path)
            valid = self.validate_board(board, path)
            if not isinstance(valid, set):
                needs_rollback = False

        # adding the line as it was randomly drawn may not be possible
        if (not needs_rollback):
            self.paths.append(path)
            return board

        return self.game


    def validate_board(self, board, path):
        """Determines whether a board contains any isolated groups of fewer
        than 3 squares"""
        clusters = []

        checked = set()
        for old_path in self.paths:
            for sq in old_path:
                checked.add(sq)
        for sq in path:
            checked.add(sq)

        print(checked)

        first_sq = None

        while(len(checked) < self.size * self.size):
            # need to do this in one loop so we can break out of it
            for i in range(self.size * self.size):
                if (i // 5, i % 5) not in checked:
                    first_sq = (i // 5, i % 5)
                    break;

            cluster = set({first_sq})
            self.bfs(board, cluster.copy(), cluster)
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

    def bfs(self, board, sqs, cluster):
        children = set()
        for sq in sqs:
            if (sq[0] != 0 and not board[sq[0] - 1][sq[1]]):
                if (sq[0] - 1, sq[1]) not in cluster:
                    children.add((sq[0] - 1, sq[1]))
                    cluster.add((sq[0] - 1, sq[1]))
            if (sq[0] != self.size - 1 and not board[sq[0] + 1][sq[1]]):
                if (sq[0] + 1, sq[1]) not in cluster:
                    children.add((sq[0] + 1, sq[1]))
                    cluster.add((sq[0] + 1, sq[1]))
            if (sq[1] != 0 and not board[sq[0]][sq[1] - 1]):
                if (sq[0], sq[1] - 1) not in cluster:
                    children.add((sq[0], sq[1] - 1))
                    cluster.add((sq[0], sq[1] - 1))
            if (sq[1] != self.size - 1 and not board[sq[0]][sq[1] + 1]):
                if (sq[0], sq[1] + 1) not in cluster:
                    children.add((sq[0], sq[1] + 1))
                    cluster.add((sq[0], sq[1] + 1))

        if (len(children)):
            self.bfs(board, children, cluster)


    def ortho_neighbors(self, point, board):
        """Finds the empty neighbors that are orthogonal to the present square"""
        neighbors = set()
        if point[0] != 0:
            if not board[point[0] - 1][point[1]]:
                neighbors.add((point[0] - 1, point[1]))
        if (point[0] != self.size - 1):
            if not board[point[0] + 1][point[1]]:
                neighbors.add((point[0] + 1, point[1]))
        if (point[1] != 0):
            if not board[point[0]][point[1] - 1]:
                neighbors.add((point[0], point[1] - 1))
        if (point[1] != self.size - 1):
            if not board[point[0]][point[1] + 1]:
                neighbors.add((point[0], point[1] + 1))

        return neighbors

    def filled_neighbors(self, point, board, path_list):
        """Finds the filled neighbors of the square, including orthogonal and
        diagonal neighbors. Counts the neighbors within the line passed as an
        argument separately from the other neighbors, which is used to prevent
        the lines doubling back upon themselves"""
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


    def rollback(self, board, path):
        print("rollback")
        last_sq = path.pop();
        board[last_sq[0]][last_sq[1]] = None;
        last_sq = path[len(path) - 1]
        board[last_sq[0]][last_sq[1]] *= 2;


    def find_pot_ends(self, board):
        """Builds up a set of empty squares on the board that either only have 1
        neighbor or are neighbors of the current endpoints"""
        one_neighbor = set()
        endpoints = set()

        for i in range(self.size):
            for j in range(self.size):
                if not board[i][j]:
                    neighbors = self.ortho_neighbors((i, j), board)
                    if len(neighbors) == 1:
                        one_neighbor.add((i, j))
                elif len(board[i][j]) == 2:
                    endpoints.add((i, j))

        pot_endpoints = one_neighbor.copy()
        for endpoint in endpoints:
            pot_endpoints = pot_endpoints.union(self.ortho_neighbors(endpoint, board))

        return pot_endpoints


    def extend_path(self, board, path, color):
        empty_neighbors = self.ortho_neighbors(path[0], board)
        # if the path can be extended at its beginning
        if empty_neighbors:
            print("extend at beginning")
            board[path[0][0]][path[0][1]] = color
            sq = empty_neighbors.pop()
            path.insert(0, sq)
            board[sq
            [0]][sq[1]] = color + color
        # if the path can be extended at its end
        else:
            print("extend at end")
            empty_neighbors = self.ortho_neighbors(path[len(path) - 1], board)
            if empty_neighbors:
                board[path[len(path) - 1][0]][path[len(path) - 1][1]] = color
                sq = empty_neighbors.pop()
                path.append(sq)
                board[sq[0]][sq[1]] = color + color


    def fill_holes(self, board, path, cluster):
        # TODO: will look through paths for adjacent endpoints that can be extended
        # then call extend_path
        # either this needs to work with the board as present, so that all paths
        # are available to check, or if working with a temp board, needs to be
        # passed the current line
        pass

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
