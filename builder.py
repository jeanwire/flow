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

    board.game = copy.deepcopy(board.onion())
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
        self.visited = set()
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

        mino_row = 0
        for i in range(row, row + len(mino)):
            mino_col = 0
            for j in range(col, col + len(mino[0])):
                if (mino[mino_row][mino_col] != 'O'):
                    temp[i][j] = re.sub('X', color, mino[mino_row][mino_col])
                    temp_visited.add((i, j))
                mino_col += 1
            mino_row += 1

        valid = self.validate_board(temp, temp_visited)
        if (valid):
            for sq in temp_visited:
                self.visited.add(sq)
        return (temp, valid)


    def onion(self):
        """Draws a line that traces along the lines already present in the board"""

        board = copy.deepcopy(self.game)
        one_neighbor = set()
        endpoints = set()
        color = self.unused_colors.pop()
        path = []
        # build up sets of points with 1 neighbor and endpoints
        # these data are used to find where to draw the next line
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

        # setting this outside the while loop allows for the second endpoint
        # to be set after the while loop breaks
        # also makes setting this endpoint easier, since the endpoints are
        # marked with the color twice while all other points have the color once
        curr_point = pot_endpoints.pop()
        path.append(curr_point)

        # marking this as an endpoint
        board[curr_point[0]][curr_point[1]] = color + color

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
            # that neighbor will have neighbors that are filled by a line
            # that is not the one the algorithm is currently drawing
            elif empty_neighbors:
                path_set = set()
                for sq in path:
                    path_set.add(sq)
                for neighbor in empty_neighbors:
                    if self.filled_neighbors(neighbor, board, path_set):
                        curr_point = neighbor
                        path.append(curr_point)
                        board[curr_point[0]][curr_point[1]] = color
                        break;
            # if there are no neighbors, line must end
            else:
                break

        board[curr_point[0]][curr_point[1]] = color + color

        # if line is only 2 sqs long, need to extend in other direction
        if len(path) < 3:
            empty_neighbors = self.ortho_neighbors(path[0], board)
            board[path[0][0]][path[0][1]] = color
            sq = empty_neighbors.pop()
            path.append(sq)
            # keep the path sqs in order
            temp = path[0]
            path[0] = path[1]
            path[1] = temp
            board[sq[0]][sq[1]] = color + color


        path_set = set()
        for sq in path:
            path_set.add(sq)
        valid = self.validate_board(board, path_set.union(self.visited))

        needs_rollback = False
        # if line has left 1 or 2 sqs open adjacent to the endpoint, need to extend the line
        # if open sqs are not adjacent to an endpoint, need to remove sqs from the path
        if isinstance(valid, set):
            board[curr_point[0]][curr_point[1]] = color;

            while(len(valid) > 0):
                neighbors = self.ortho_neighbors(curr_point, board)
                for sq in valid:
                    if sq in neighbors:
                        curr_point = sq
                        board[curr_point[0]][curr_point[1]] = color
                        path.append(curr_point)
                        break

                prev_valid = valid;
                valid = valid.difference({curr_point})

                # if sq is not a neighbor of the endpoint, will need to "roll back" the line
                if prev_valid == valid:
                    needs_rollback = True
                    break

            board[curr_point[0]][curr_point[1]] = color + color

        while (needs_rollback):
            self.rollback(board, path)
            path_set = set()
            for sq in path:
                path_set.add(sq)
            valid = self.validate_board(board, path_set.union(self.visited))
            if not isinstance(valid, set):
                needs_rollback = False

        for sq in path:
            self.visited.add(sq)
        return board


    def validate_board(self, board, visited):
        """Determines whether a board contains any isolated groups of fewer
        than 3 squares"""
        clusters = []

        checked = visited.copy()
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

    def filled_neighbors(self, point, board, path):
        """Finds the filled neighbors of the square, including orthogonal and
        diagonal neighbors. Only counts neighbors if they are not in the line
        currently being drawn"""
        neighbors = []
        # row above
        if point[0] != 0:
            if board[point[0] - 1][point[1]] and ((point[0] - 1,point[1]) not in path):
                neighbors.append((point[0] - 1,point[1]))
            if point[1] != 0 and board[point[0] - 1][point[1] - 1] and ((point[0] - 1,point[1] - 1) not in path):
                neighbors.append((point[0] - 1,point[1] - 1))
            if point[1] != self.size - 1 and board[point[0] - 1][point[1] + 1] and ((point[0] - 1,point[1] + 1) not in path):
                neighbors.append((point[0] - 1,point[1] + 1))
        # row below
        if point[0] != self.size - 1:
            if board[point[0] + 1][point[1]] and ((point[0] + 1,point[1]) not in path):
                neighbors.append((point[0] + 1,point[1]))
            if point[1] != 0 and board[point[0] + 1][point[1] - 1] and ((point[0] + 1,point[1] - 1) not in path):
                neighbors.append((point[0] + 1,point[1] - 1))
            if point[1] != self.size - 1 and board[point[0] + 1][point[1] + 1] and ((point[0] + 1,point[1] + 1) not in path):
                neighbors.append((point[0] + 1,point[1] + 1))
        # left sq
        if point[1] != 0 and board[point[0]][point[1] - 1] and ((point[0],point[1] - 1) not in path):
            neighbors.append((point[0],point[1] - 1))
        # right sq
        if point[1] != self.size - 1 and board[point[0]][point[1] + 1] and ((point[0],point[1] + 1) not in path):
            neighbors.append((point[0],point[1] + 1))

        return neighbors


    def rollback(self, board, path):
        last_sq = path.pop();
        board[last_sq[0]][last_sq[1]] = None;
        last_sq = path[len(path) - 1]
        board[last_sq[0]][last_sq[1]] *= 2;


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
