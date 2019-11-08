class Point(object):
    def __init__(self, x, y, color, end=False):
        self.x = x
        self.y = y
        self.end = end
        self.color = color
        self.next = []
        self.previous = None

    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y and self.end == p2.end

    def __str__(self):
        return f'({self.x}, {self.y}), End: {self.end}'

class Tree(object):
    def __init__(self):
        self.root = None
        self.curr_branch = None
        # paths is a collection of pointers to the first endpoints of the paths
        self.paths = []


    def push(self, point):
        if self.root:
            for child in self.curr_branch.next:
                if child == point:
                    return False
            self.curr_branch.next.append(point)
            point.previous = self.curr_branch
            self.curr_branch = point
            return True
        self.root = point
        self.curr_branch = self.root
        self.paths.append(self.root)
        return True


    def push_start_of_line(self, point):
        start = self.paths.pop()
        # if endpoint has already been attempted, return false
        if (start.previous):
            for child in start.previous.next:
                if child == point:
                    self.paths.append(start)
                    return False

        # otherwise, insert new point into tree and return true
        start.end = False
        self.paths.append(point)
        if (start.previous):
            start.previous.next.append(point)
        # if adding to the start of the mino, need to change the tree root
        else:
            self.root = point
        point.next.append(start)
        start.previous = point
        return True


    def pop(self):
        '''Does not remove a node from the tree; moves the pointer to the current
        node to its previous node.'''
        self.curr_branch = self.curr_branch.previous


    def visited_sqs(self):
        '''Returns a set of indices on the board that are filled'''
        visited = set()
        node = self.curr_branch
        while (node):
            visited.add((node.x, node.y))
            node = node.previous
        return visited


    def most_recent_path(self):
        '''Returns an array containing the indices of the most recent path
        added to the tree, if any paths have been added.'''
        if not self.paths:
            return None

        path = []
        node = self.curr_branch
        endpoint = self.paths[len(self.paths) - 1]
        while (node != endpoint):
            path.append((node.x, node.y))
            node = node.previous

        path.append((node.x, node.y))

        return path


    def all_paths(self):
        '''Returns an array of arrays containing all paths'''

        paths = []
        node = self.curr_branch
        index = len(self.paths) - 1
        while (node):
            path = []
            endpoint = self.paths[index]

            while (node != endpoint):
                path.append((node.x, node.y))
                node = node.previous

            # appending endpoint
            path.append((node.x, node.y))
            paths.append(path)

            # setup for next loop iteration
            node = node.previous
            index -= 1


        return paths
