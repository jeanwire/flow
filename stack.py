class Point(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.end = False
        self.color = color
        self.next = []
        self.previous = Null

    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y

class Stack(object):
    def __init__(self, line):
        self.root = Point(line[0][0], line[0][1], 'r')
        self.root.end = True
        self.curr_branch = self.root


    def push(self, point):
        for child in curr_branch.next:
            if child == point:
                return False
        self.curr_branch.next.append(point)
        point.previous = self.curr_branch
        self.curr_branch = point
        return True 


    def pop(self):
        self.curr_branch = self.curr_branch.previous
