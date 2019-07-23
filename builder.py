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
            temp_board, inserted, mino_loc = board.insert(mino)

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
        self.visited = {}
        for i in range(size):
            for j in range(size):
                self.visited[(i, j)] = False
        self.complete = False
        self.unused_colors = ['m', 'p', 'a', 'o', 'y', 'b', 'g', 'r']


    def insert(self, mino):
        row = random.randint(0, self.size - len(mino))
        col = random.randint(0, self.size - len(mino[0]))

        color = self.unused_colors.pop()
        temp, valid = self.mino_in_board(mino, row, col, color)


        if (not valid and row + 1 < self.size - len(mino)):
            temp, valid = self.mino_in_board(mino, row + 1, col, color)
        elif (not valid and col + 1 < self.size - len(mino[0])):
            temp, valid = self.mino_in_board(mino, row, col + 1, color)
        elif (not valid and row - 1 >= 0):
            temp, valid = self.mino_in_board(mino, row - 1, col, color)
        elif (not valid and col - 1 >= 0):
            temp, valid = self.mino_in_board(mino, row, col - 1, color)
        return (temp, valid, (row, col))


    def mino_in_board(self, mino, row, col, color):
        temp = copy.deepcopy(self.game)
        temp_visited = []

        mino_row = 0
        for i in range(row, row + len(mino)):
            mino_col = 0
            for j in range(col, col + len(mino[0])):
                if (mino[mino_row][mino_col] != 'O'):
                    temp[i][j] = re.sub('X', color, mino[mino_row][mino_col])
                    temp_visited.append((i, j))
                mino_col += 1
            mino_row += 1

        valid = self.validate_board(temp, temp_visited)
        if (valid):
            for sq in temp_visited:
                self.visited[sq] = True
        return (temp, valid)


    def onion(self):
        """Draws a line that traces along the lines present in the board"""

        board = copy.deepcopy(self.game)
        one_neighbor = set()
        endpoints = set()
        color = self.unused_colors.pop()
        path = set()
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

        pot_endpoints = one_neighbor
        for endpoint in endpoints:
            pot_endpoints = pot_endpoints.union(self.ortho_neighbors(endpoint, board))

        # setting this outside the while loop allows for the second endpoint
        # to be set after the while loop breaks
        # also makes setting this endpoint easier, since the endpoints are
        # marked with the color twice while all other points have the color once
        curr_point = pot_endpoints.pop()
        path.add(curr_point)

        # marking this as an endpoint
        board[curr_point[0]][curr_point[1]] = color + color

        # randomly ends after path is 3 sqs long and <= 10 sqs long
        # does this generate a different number each loop?
        for i in range(0, 5):
            empty_neighbors = self.ortho_neighbors(curr_point, board)
            print(empty_neighbors)
            # if there is only one neighbor, don't need to perform any further analysis
            if len(empty_neighbors) == 1:
                print("one empty neighbor")
                curr_point = empty_neighbors.pop()
                path.add(curr_point)
                board[curr_point[0]][curr_point[1]] = color
            # if there are multiple neighbors, need to determine which one
            # allows for "onion" behavior
            # that neighbor will have neighbors that are filled by a line
            # that is not the one the algorithm is currently drawing
            elif empty_neighbors:
                print("multiple empty neighbors")
                for neighbor in empty_neighbors:
                    if self.filled_neighbors(neighbor, board, path):
                        print("appending to list")
                        curr_point = neighbor
                        path.add(curr_point)
                        board[curr_point[0]][curr_point[1]] = color
                        break;
            # if there are no neighbors, line must end
            else:
                break

        board[curr_point[0]][curr_point[1]] = color + color

        return board


    def validate_board(self, board, visited):
        clusters = []

        checked = visited.copy()
        first_sq = None

        while(len(checked) < self.size * self.size):
            # need to do this in one loop so we can break out of it
            for i in range(self.size * self.size):
                try:
                    checked.index((i // 5, i % 5))
                except ValueError:
                    first_sq = (i // 5, i % 5)
                    break;

            cluster = [first_sq]
            self.bfs(board, cluster, cluster)
            if cluster:
                clusters.append(cluster)
                checked += cluster
            # reset this value
            first_sq = None

        for cluster in clusters:
            if len(cluster) <= 2:
                return False

        return True

    def bfs(self, board, sqs, cluster):
        children = []
        for sq in sqs:
            if (sq[0] != 0 and not board[sq[0] - 1][sq[1]]):
                try:
                    cluster.index((sq[0] - 1, sq[1]))
                except ValueError:
                    children.append((sq[0] - 1, sq[1]))
                    cluster.append((sq[0] - 1, sq[1]))
            if (sq[0] != self.size - 1 and not board[sq[0] + 1][sq[1]]):
                try:
                    cluster.index((sq[0] + 1, sq[1]))
                except ValueError:
                    children.append((sq[0] + 1, sq[1]))
                    cluster.append((sq[0] + 1, sq[1]))
            if (sq[1] != 0 and not board[sq[0]][sq[1] - 1]):
                try:
                    cluster.index((sq[0], sq[1] - 1))
                except:
                    children.append((sq[0], sq[1] - 1))
                    cluster.append((sq[0], sq[1] - 1))
            if (sq[1] != self.size - 1 and not board[sq[0]][sq[1] + 1]):
                try:
                    cluster.index((sq[0], sq[1] + 1))
                except:
                    children.append((sq[0], sq[1] + 1))
                    cluster.append((sq[0], sq[1] + 1))

        if (len(children)):
            self.bfs(board, children, cluster)


    def ortho_neighbors(self, point, board):
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
        neighbors = []
        print("path: ", path)
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
