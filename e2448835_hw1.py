import copy
class State:
    """State class that represents the state of the puzzle"""
    def __init__(self, matrix, parent, g = None, h = None):
        self.matrix = matrix
        self.g = g # cost to reach the current state from the initial state
        self.h = h # heuristic cost
        if g is not None:
            self.f = g + h
        self.parent = parent

    def __eq__ (self, other):
        return self.matrix == other.matrix
    def __str__(self):
        st = ""
        for row in self.matrix:
            for index, element in enumerate(row):
                if index == 3:
                    st += element + "\n"
                else:
                    st += element + " "
        return st
def print_success(state:State):
    """Prints the path from the initial state to the goal state"""
    st = str(state)
    while state.parent:
        state = state.parent
        st = str(state) + "\n" + st
    st = "SUCCESS\n\n" + st
    return st[:-1]


def find_empty(matrix):
    """Finds the position of the empty cell in the matrix"""
    return [(i, j) for i in range(4) for j in range(4) if matrix[i][j] == "_"][0]

def expand(state, goal, is_a_star = True):
    """Expands the current state and returns the new states"""
    i, j = find_empty(state.matrix)
    frontier = []
    if i < 3: #move up
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i+1][j] = new_matrix[i+1][j], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+2, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    if i > 0: #move down
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i-1][j] = new_matrix[i-1][j], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+2, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    if j < 3: #move left
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i][j+1] = new_matrix[i][j+1], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+2, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    if j > 0: #move right
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i][j-1] = new_matrix[i][j-1], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+2, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    if i < 2: #move up twice
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i+2][j] = new_matrix[i+2][j], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+3, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    if i > 1: #move down twice
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i-2][j] = new_matrix[i-2][j], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+3, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    if j < 2: #move left twice
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i][j+2] = new_matrix[i][j+2], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+3, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    if j > 1: #move right twice
        new_matrix = copy.deepcopy(state.matrix)
        new_matrix[i][j], new_matrix[i][j-2] = new_matrix[i][j-2], new_matrix[i][j]
        if is_a_star:
            new_state = State(new_matrix, state, state.g+3, find_h(new_matrix, goal.matrix))
        else:
            new_state = State(new_matrix, state)
        frontier.append(new_state)
    return frontier

def a_star (init, goal, max_cost):
    """
            explored <_ an empty set
        frontier <- list that contains a node for problem's initial state
        loop
            if frontier is empty then return Failure
            x <- arg min{f(y) | y in frontier}
            if State[x] is a goal state then return x
            if there is no node y in explored such that
                State[y] = State[x] and f(y) <= f(x )
            then
                add x to explored
                expand x and add the new nodes to frontier
"""
    frontier = [init]
    explored = []
    _result = None
    while frontier:
        x = min(frontier, key=lambda x: x.f)
        frontier.remove(x)
        if x.f > max_cost:
            return "FAILURE"
        if x == goal:
            _result = print_success(x)
            return _result
        if not check_explored(x, explored):
            explored.append(x)
            frontier += expand(x, goal)
    return "FAILURE"

def check_explored(x, explored):
    """Checks if there is a node in the explored set that has the same state as x and has a lower cost"""
    for y in explored:
        if y == x and y.f <= x.f:
            return True
    return False
def limited_depth_search(node, goal, limit):
    """
    if node contains a goal state then return the corresponding solution
    else if limit = 0 then return Cutoff
    else
        notfound <- Failure /* what to return if we don't find a solution */
        for each y in Expand(node) do
            result <- Limited-Depth-Search(y, problem, limit-1)
            if result is a solution then return result
            else if result = Cutoff then notfound <- Cutoff
        return notfound
    """
    notfound = ""
    if node == goal:
        return node
    if limit == 0:
        return "Cutoff"
    notfound = "failure"
    for y in expand(node, goal, False):
        _result = limited_depth_search(y, goal, limit-1)
        if isinstance(_result, State):
            return _result
        if _result == "Cutoff":
            notfound = "Cutoff"
    return notfound
def dfids (init, goal, max_depth):
    """
    node <- node for problem's initial state
    for limit 0 to max_depth do
    result <- Limited-Depth-Search(node, goal, limit)
    if result != Cutoff then return result
    """
    for limit in range(max_depth+1):
        _result = limited_depth_search(init, goal, limit)
        if isinstance(_result, State):
            return print_success(_result)
    return "FAILURE"

def find_goal(item, goal) -> tuple[int, int]:
    """ Finds the position of the item in the goal state """
    for i in range(4):
        for j in range(4):
            if goal[i][j] == item:
                return i, j
def find_h(matrix, goal):
    """Finds the heuristic cost of the current state"""
    h = 0
    for i in range(4):
        for j in range(4):
            item = matrix[i][j]
            if item != "_" :
                goal_i, goal_j = find_goal(item, goal)
                h += abs(i - goal_i) + abs(j - goal_j)
    return h


def parse_input():
    """Parses the input and returns the result"""
    lines = []
    for _ in range(10):
        lines.append(input())
    if lines[0] == "A*" :
        max_cost = int(lines[1])
        init_matrix = []
        goal_matrix = []
        for i in range(4):
            init_matrix.append(list(lines[2+i].split()))
            goal_matrix.append(list(lines[6+i].split()))
        init_state = State(init_matrix, None, 0, find_h(init_matrix, goal_matrix))
        goal_state = State(goal_matrix, None, 0, 0)
        return a_star(init_state, goal_state, max_cost)
    if (lines[0] == "DFIDS" or lines[0] == "DIFDS"):
        max_depth = int(lines[1])
        init_matrix = []
        goal_matrix = []
        for i in range(4):
            init_matrix.append(list(lines[2+i].split()))
            goal_matrix.append(list(lines[6+i].split()))
        init_state = State(init_matrix, None, 0, find_h(init_matrix, goal_matrix))
        goal_state = State(goal_matrix, None, 0, 0)
        return dfids(init_state, goal_state, max_depth)
    return "INVALID INPUT"

result = parse_input()

print(result, end="")
