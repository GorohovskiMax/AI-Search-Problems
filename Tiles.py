from Node import Node
import numpy as np
from collections import deque 
import heapq


#Global Variables:
goal_matrix = np.array([0,1,2,3,4,5,6,7,8]).reshape(3,3)
moves = [(-1,0),(1,0),(0,-1),(0,1)] # The actions = UP,DOWN,LEFT,RIGHT 


# Recieve input from the user (sequence of 9 tiles) and return a node with a 3x3 matrix of tiles representing the 8-puzzle
def get_init_state():
    input_state = list((map(int, input("\nEnter the initial state of the puzzle: \n").strip().split())))
    matrix = np.array(input_state).reshape(3,3)
    node = Node(matrix)
    return node


# Recieve the current state (matrix) and return all the possible moves from this state by making a legal move (Node instances)
def generate_next_states(node):
    zero_position = np.where(node.matrix == 0) #find the location of the 0 digit (blank tile)
    row,col = zero_position[0][0], zero_position[1][0]
    possible_states = []

    for move in moves:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = np.copy(node.matrix) #make a copy to generate a new state
            new_state[row,col], new_state[new_row,new_col] = new_state[new_row,new_col], new_state[row][col] # Replace the numerated tile's location to be the 0's location (made an action)
            possible_states.append(Node(new_state, node, new_state[row,col], move, node.cost + 1)) # New node has a new matrix based on the action and the moved tile, it's parent is the node we expanded and it has the parent's path-cost + 1 (cost of a move)

    return possible_states        


# Method to display the algorithm name, nodes expanded and the path that is made to reach the goal
def display_algorithm_results(algorithm, count, path):
    print(f"\n{algorithm}: \n")
    print(f"Nodes Expanded: {count}\n")
    print(f"Path to Goal: {path}\n")
    

# BFS implementation - Book Algorithm interpretation 
def BFS(node):
    frontier = deque([node])
    reached = set(tuple(map(tuple, node.matrix))) # Set made out of tuples of tuples of matrices (nodes are not iterables)
    count = 0
    
    if np.array_equal(node.matrix, goal_matrix):
        display_algorithm_results("BFS",count,node.display_path())
        return 

    while frontier:
        current_node = frontier.popleft()
        count+=1

        for next_node in generate_next_states(current_node): #For each node in the new list of generated nodes
            if np.array_equal(next_node.matrix, goal_matrix):
             display_algorithm_results("BFS",count,next_node.display_path())
             return 
            
            if tuple(map(tuple, next_node.matrix)) not in reached: # Check if the given matrix has already been reached to prevent loop-overs
                reached.add(tuple(map(tuple, next_node.matrix)))
                frontier.append(next_node)

    return None            


#IDDFS implementation - Recursive interpretation
def IDDFS(node):
    def DLS(node, depth, visited, count):
        # Base Case:
        if depth == 0 and np.array_equal(node.matrix, goal_matrix):
            display_algorithm_results("IDDFS",count[0],node.display_path())
            return node
        
        
        elif depth > 0:
            visited.add(tuple(map(tuple, node.matrix))) # Indicate that we have seen the current node in the branch
            for next_node in generate_next_states(node):
                count[0]+=1
                if tuple(map(tuple, next_node.matrix)) not in visited:
                    result = DLS(next_node, depth - 1, visited, count)
                    if result:
                         return result
            visited.remove(tuple(map(tuple, node.matrix))) # Release as we want to allow other branches to explore this state

        return None # No solution at current depth           

    depth = 0
    count = [0] # We want to count all the nodes that were expanded within depth levels, regardless of whether we reached it already

    while True: # from depth = 0 to infinity
        visited = set() 
        result = DLS(node, depth, visited, count)
        if result:
            return result
        depth+=1 

# Heuristic 1: Linear Conflict
def linear_conflict(node):
    def manhattan_distance(matrix, goal_matrix): # Used to count the total manhattan distances
        total_manhattan = 0
        for num in range(1,9):
            x,y = np.where(matrix == num)
            xGoal,yGoal = np.where(goal_matrix == num)
            total_manhattan +=abs(xGoal[0] - x[0]) + abs(yGoal[0] - y[0])

        return total_manhattan

    conflicts = 0
    goal_tile_positions = {goal_matrix[row][col] : (row,col) for row in range(3) for col in range(3)} #Using dictionary to easily access the indices of a number within the goal matrix
    for row in range(3): # Row iterations
        row_goal = goal_matrix[row, :] 
        current_row = node.matrix[row, :]
        for i in range(3):
            for j in range(i+1, 3):
             tileX, tileY = goal_tile_positions[goal_matrix[row][i]][1], goal_tile_positions[goal_matrix[row][j]][1] # Get the tile at col 'i' and tile at col 'j' within the same row
             if current_row[i] in row_goal and current_row[j] in row_goal and tileX > tileY: #If both tiles are supposed to be in the same exact goal row but one "blocks" the other from being in the correct spot, then there is a linear conflict
                conflicts+=1

    for col in range(3): #Col iterations
        col_goal = goal_matrix[:, col] 
        current_col = node.matrix[:, col]
        for i in range(3):
            for j in range(i+1, 3):
                tileX, tileY = goal_tile_positions[goal_matrix[i][col]][0], goal_tile_positions[goal_matrix[j][col]][0] # Get the tile at row 'i' and tile at row 'j' within the same column
                if current_col[i] in col_goal and current_col[j] in col_goal and tileX > tileY: #If both tiles are supposed to be in the same exact goal column but one "blocks" the other from being in the correct spot, then there is a linear conflict
                    conflicts+=1           
    
    return 2 * conflicts + manhattan_distance(node.matrix, goal_matrix) 

# Heuristic 2: Euclidean Distance
def euclidean_distance(node):
        total_euclidean = 0
        for num in range(1,9):
            x,y = np.where(node.matrix == num)
            xGoal,yGoal = np.where(goal_matrix == num)
            total_euclidean +=np.sqrt((x[0]-xGoal[0])**2 + (y[0] - yGoal[0])**2) # Distance Formula for two points 

        return total_euclidean


# GBFS Algorithm - Based on Best-First-Search Algorithm but uses the heuristic 'h' as it's function
def GBFS(node):
    frontier = []
    reached = {} 
    count = 0
    node.heuristic = euclidean_distance(node) # Heuristic 2
    heapq.heappush(frontier, (node.h(), node)) 
    reached[tuple(map(tuple, node.matrix))] = node # avoid looping over visited states
    while frontier:
        _, current_node = heapq.heappop(frontier) # Ignore the heuristic values and get the node from the priority queue

        if np.array_equal(current_node.matrix, goal_matrix):
            display_algorithm_results("GBFS",count,current_node.display_path())
            return 
        
        for next_node in generate_next_states(current_node): 
            count+=1
            if tuple(map(tuple, next_node.matrix)) not in reached or next_node.cost < reached[tuple(map(tuple, next_node.matrix))].cost: # If we haven't visited this matrix yet or we can get this matrix but with a better path-cost
             next_node.heuristic = euclidean_distance(next_node)
             reached[tuple(map(tuple, next_node.matrix))] = next_node 
             heapq.heappush(frontier, (next_node.h(), next_node))

    return None

# A* Algorithm - Based on Best-First-Search Algorithm but uses the heuristic 'h' + cost of path as it's function
def A_star(node):
    frontier = [] 
    reached = {} 
    count = 0
    node.heuristic = linear_conflict(node) # Heuristic 1
    heapq.heappush(frontier, (node.f(), node))
    reached[tuple(map(tuple, node.matrix))] = node # avoid looping over visited states

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if np.array_equal(current_node.matrix, goal_matrix):
            display_algorithm_results("A*",count,current_node.display_path())
            return 
        
        for next_node in generate_next_states(current_node):
            count+=1
            if tuple(map(tuple, next_node.matrix)) not in reached or next_node.cost < reached[tuple(map(tuple, next_node.matrix))].cost:
             next_node.heuristic = linear_conflict(next_node)
             reached[tuple(map(tuple, next_node.matrix))] = next_node
             heapq.heappush(frontier, (next_node.f(), next_node))

    return None


def main(): 
    str_input = get_init_state()
    BFS(str_input)    
    IDDFS(str_input)
    GBFS(str_input)
    A_star(str_input)

if __name__ == '__main__':
    main()    