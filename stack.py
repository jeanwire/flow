class Point(object):
    def __init__(self, x, y, color, end=False):
        self.x = x
        self.y = y
        self.end = end
        self.color = color
        self.next = []
        self.previous = None

    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y

class Stack(object):
    def __init__(self, line):
        self.root = Point(line[0][0], line[0][1], 'r', True)
        self.curr_branch = self.root
        for i in range(1, len(line) - 1):
            self.push(Point(line[i][0], line[i][1], 'r'))
        i = len(line) - 1
        self.push(Point(line[i][0], line[i][1], 'r', True))


    def push(self, point):
        for child in self.curr_branch.next:
            if child == point:
                return False
        self.curr_branch.next.append(point)
        point.previous = self.curr_branch
        self.curr_branch = point
        return True


    def pop(self):
        self.curr_branch = self.curr_branch.previous
