import os
import json
# import ./minos.json


def main():
    minos_dict = import_minos()
    board = Board(5)
    board.build_board()

    node = board.game

    while (node.down):
        print(node.value)
        node = node.down

    while(node):
        print(node.value)
        node = node.right


    # choose mino(s)
    # insert mino(s) in board
    # build lines around mino(s)
    # validate board
    # when board is completed, write to file in json format


class Board(object):
    def __init__(self, size):
        self.size = size
        self.game = None

    def build_board(self):
        count = 0
        prevRow = None

        for i in range(self.size):
            prevNode = Node(count)
            count += 1
            firstNode = prevNode

            if (i):
                prevRow.down = firstNode
                firstNode.up = prevRow
                prevRow = prevRow.right

            if (self.game is None):
                self.game = firstNode

            for j in range(1, self.size):
                currNode = Node(count)
                count += 1
                prevNode.right = currNode
                currNode.left = prevNode

                # not top row
                if (i):
                    prevRow.down = currNode
                    currNode.up = prevRow
                    prevRow = prevRow.right

                prevNode = currNode

            prevRow = firstNode



class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.up = None
        self.down = None


def import_minos():
    with open('minos.json') as minos_file:
        json_data = json.load(minos_file)
        return json_data


if __name__ == '__main__':
    main()
