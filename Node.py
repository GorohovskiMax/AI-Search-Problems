
class Node:
    def __init__(self, matrix, parent=None, moved_tile=None, action=None, cost=0, heuristic=0):
        self.matrix = matrix
        self.parent = parent
        self.moved_tile = moved_tile
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
        
    # Get the path from the goal node to the root and display the visited moved tiles
    def display_path(self):
        current_node = self
        tiles = []

        while current_node is not None:
            if current_node.moved_tile is not None:
                tiles.append(current_node.moved_tile)
            current_node = current_node.parent

        tiles.reverse()
        return " -> ".join(map(str, tiles))

    # Representing the function as f = g + h where g is the cost and h is the heuristic
    def f(self):
        return self.cost + self.heuristic

    # Represeting the function as f = h for GBFS Algorithm
    def h(self):
        return self.heuristic
    
    # less-than method for the priority-queue
    def __lt__(self, other):
        return self.f() < other.f()