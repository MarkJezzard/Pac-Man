from queue import PriorityQueue

tiles_nodes = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 8, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 1, 1, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 8, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 8, 0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 8, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 8, 0, 0, 0, 0, 8, 1, 1, 8, 0, 0, 8, 1, 1, 8, 0, 0, 8, 1, 1, 8, 0, 0, 0, 0, 8, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 8, 0, 0, 8, 1, 1, 1, 1, 1, 1, 1, 1, 8, 0, 0, 8, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 8, 0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 8, 1, 1, 8, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 8, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 8, 0, 8, 1, 1, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 1, 1, 8, 0, 8, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 8, 0, 8, 0, 0, 8, 1, 1, 8, 0, 0, 8, 1, 1, 8, 0, 0, 8, 1, 1, 8, 0, 0, 8, 0, 8, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Node:
    def __init__(self, position):
        self.row = position[0]
        self.column = position[1]
        self.position = position  # row, column
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")
        self.previous = None
        self.neighbours = []  # list of positions of adjacent nodes

    def set_g(self, g):
        self.g = g
        self.f = self.g + self.h

    def dist_to_node(self, node):
        y1, x1 = self.row, self.column
        y2, x2 = node
        return abs(x1 - x2) + abs(y1 - y2)

    def get_neighbours(self, grid):
        # check nodes above
        i = self.row
        carry_on = True
        while grid[i-1][self.column] != 1 and carry_on:
            if grid[i-1][self.column] == 8:
                self.neighbours.append((i-1, self.column))
                carry_on = False
            else:
                i -= 1

        # to the left
        i = self.column
        carry_on = True
        while grid[self.row][i - 1] != 1 and carry_on:
            if grid[self.row][i - 1] == 8:
                self.neighbours.append((self.row, i - 1))
                carry_on = False
            else:
                i -= 1

        # below
        i = self.row
        carry_on = True
        while grid[i+1][self.column] != 1 and carry_on:
            if grid[i+1][self.column] == 8:
                self.neighbours.append((i+1, self.column))
                carry_on = False
            else:
                i += 1

        # to the right
        i = self.column
        carry_on = True
        while grid[self.row][i+1] != 1 and carry_on:
            if grid[self.row][i+1] == 8:
                self.neighbours.append((self.row, i+1))
                carry_on = False
            else:
                i += 1

        # want to prioritise in order: up, right, left, down
        # give count so that order is kept if f value same


def a_star(start, end, node_grid):
    # start and end positions become nodes in the tiles grid
    node_grid[start[0]][start[1]] = 8
    node_grid[end[0]][end[1]] = 8

    count = 0  # count used for direction priority (if new neighbours have same f value, will be prioritised u>l>d>r)

    # initialising 'open' and 'closed'
    open_pq = PriorityQueue()  # Nodes to consider. Holds f(n) value with node position
    open_positions = []  # List of generated node positions for object lookup
    open_objects = []  # List of generated node objects in open list (for updating neighbour f values/previous)
    closed_positions = []  # List of node positions that have been searched
    # Whenever add/remove from open_pq, add/remove from open_positions, & add/remove from open_objects
    # Therefore indexes will match up so can use index of node position to find node object

    # start node becomes current node
    # outside main loop since special case
    current = Node(start)
    current.set_g(0)
    current.h = current.dist_to_node(end)
    current.f = current.h

    # add current to 'open'
    open_objects.append(current)
    open_positions.append(current.position)
    open_pq.put((current.f, count, current.position))

    while True:
        # getting next current node
        current_position = open_pq.get()[2]
        index = open_positions.index(current_position)
        current = open_objects[index]

        if current.position == end:  # the algorithm terminates when end is at the front of the priority queue
            break

        current.get_neighbours(node_grid)
        for neighbour_position in current.neighbours:
            # only searches neighbours that haven't already been searched
            if neighbour_position not in closed_positions:
                # create new node if neighbour has not been found previously
                if neighbour_position not in open_positions:
                    open_positions.append(neighbour_position)
                    neighbour = Node(neighbour_position)
                    neighbour.h = neighbour.dist_to_node(end)
                    neighbour.previous = current
                    neighbour.set_g(current.g + current.dist_to_node(neighbour_position))
                    open_objects.append(neighbour)
                    count += 1
                    open_pq.put((neighbour.f, count, neighbour.position))

                elif neighbour_position in open_positions:
                    index = open_positions.index(neighbour_position)
                    neighbour = open_objects[index]
                    # find node w pos of neighbour (node has already been created so f_value is needed for comparison)
                    temp_g = current.g + current.dist_to_node(neighbour_position)
                    if temp_g < neighbour.g:
                        neighbour.previous = current
                        neighbour.set_g(temp_g)

        # removing current from open and adding current to closed
        open_positions.remove(current.position)
        open_objects.remove(current)
        closed_positions.append(current.position)

        if not open_positions:  # if open is empty and not reached end
            return 'NO PATH'

    path = [((current.position[0] * 8 + 3), (current.position[1] * 8 + 3))]
    # creates path array that starts with current position inside

    while current.previous is not None:
        path.append(((current.previous.position[0] * 8 + 3), (current.previous.position[1] * 8 + 3)))
        current = current.previous

    return path
