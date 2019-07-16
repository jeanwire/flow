import os
import json
import random
# import ./minos.json


def main():
    minos_dict = import_minos()
    board = Board(5)
    mino = select_mino(minos_dict)
    print(mino)
    if (len(mino[0]) < board.size):
        board.insert(mino)

    print(board.game)

    # insert mino(s) in board
    # build lines around mino(s)
    # validate board, repeat adding lines if necessary
    # when board is completed, write to file in json format


class Board(object):
    def __init__(self, size):
        self.size = size
        self.game = []
        for i in range(size):
            self.game.append([None, None, None, None, None])
        self.complete = False


    def insert(self, mino):
        row = random.randint(0, self.size - len(mino))
        col = random.randint(0, self.size - len(mino[0]))
        mino_row = 0
        mino_col = 0
        for i in range(row, row + len(mino)):
            mino_col = 0
            for j in range(col, col + len(mino[0])):
                if (mino[mino_row][mino_col] != 'O'):
                    self.game[i][j] = mino[mino_row][mino_col]
                mino_col += 1
            mino_row += 1


class Node(object):
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.left = None
        self.right = None
        self.up = None
        self.down = None


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
