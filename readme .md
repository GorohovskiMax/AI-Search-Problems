# 8-Puzzle Problem Solver 🧩 

## Table of Contents
- [Author📝](#author📝)
- [Overview📄](#overview📄)
- [Data Structures🗂️](#data-structures-🗂️)
- [Implementations📘](#implementations📘)
- [Heuristics🧠](#heuristics-🧠)

## Author📝
This Project was submitted by **Maxim Gorohovski, ID: 212614176**


## Overview📄
The Project folder includes two Python files: `Node.py` and `Tiles.py`. These are used to implement an 8-puzzle solver using the search algorithms: **BFS (Breadth-First Search)**, **IDDFS (Iterative Deepening Depth-First Search)**, **GBFS (Greedy Best-First Search)** and **A***. The program receives a sequence of 9 digits (8 numbers numerated from 1 - 8 and an additional 0 representing the blank tile) and transforms it into a node with a matrix representing that sequence. The program then iterates through every algorithm and returns the **algorithm name, how many nodes were expanded to reach the goal and what is the path that we have to make to reach the goal**

## File Breakdown:
1. **Node.py**:
    - Contains the implementation of nodes that allow transitioning from one puzzle state to another via an action

    - **Functions**:
      - `display_path`: Displays the sequence of tile movements (from initial state to the goal state) needed to reach the goal state (solved puzzle)
      
      - `f`: Represents f(x), which is the total path cost g(x) summed with a heuristic value h(x) for a given puzzle state. This function is primarily used in A*
      
      - `h`: Represents h(x), a heuristic value assigned to a given puzzle state. This function is used in GBFS and A*

      - `__lt__`: A necessary function for implementing a priority queue

2. **Tiles.py**:
   - Contains the implementation of the search algorithms, puzzle-related functions, print functions, main function, data structures, and library usage

   - **Global Variables**:
     - `goal_matrix`: The target configuration of the puzzle as a 3 x 3 Numpy matrix

     - `moves`: A list of moves (**up**, **down**, **left**, **right**) represented as (x,y) coordinates

    - **Functions**:

       - `get_init_state`: Takes input from the user (a sequence of 9 values where 0 represents the blank tile), converts it into a 3x3 matrix, initializes a node with the given matrix, and returns the node

       - `generate_next_state`: Receives a node, iterates over all possible moves based on the blank tile's position, and returns a list of nodes with the relevant transitions applied

       - `display_algorithm_results`:  neatly displays the desired output—algorithm name (abbreviated), number of nodes expanded and the solution path (in separate lines)


## Data Structures 🗂️
- **Nodes**:
  - Each node contains:
    - **Matrix**: Representation of the puzzle
     
    - **Parent Node**: Default is `None`

    - **Moved Tile**: The tile moved from the previous puzzle state to the current state, default is `None`

    - **Action**: The action taken to transition to the current puzzle state, default is `None`

    - **Cost**: Path cost from the start of the puzzle to the current node, default is `0`

    - **Heuristic**: Value assigned by a heuristic function, default is `0`



- **Deque**: Used in **BFS** as the data structure for the frontier

- **Heapq**: A priority queue used for **GBFS** and **A*** to handle nodes based on a certain priority values

- **Numpy**: Utilized for easier matrix representation of 3x3 grids and simplified access to rows and columns

## Implementations📘
   - **State Space Representation**:

     - Before implementing the algorithms we must understand what are the possible states and moves of the puzzle:
    
        - **Possible States**: Defined to be the positions of the eight numerated tiles and the blank tile

        - **Possible Moves**: Up, Down, Left and Right (referring to moves of the blank tile)


1. **Breadth First Search (BFS)** 🌐:

    - A search algorithm that explores nodes level by level (breadth-wise) and finds the path from the initial state to the goal state. **BFS** guarantees that paths are checked in order of distance from the initial state

    - **Implementation**: 
      
      - Based mostly on the textbook implementation (Page 95)

      - Uses `deque` for the `frontier` to allow breadth-wise exploration

      - A `set` named `reached` is used to track visited matrices (values are stored as tuples of tuples of matrices to avoid hashing issues)

      - If the given matrix equals the goal matrix, it returns the number of nodes expanded and the path. If not, explore other states by making a move

      - If no solution is found, return None

    - **Optimality**:  Yes, **BFS** guarantees finding the optimal path from the initial state to the goal state.

2. **Iterative Deepening Depth-First Search (IDDFS)** 🔄:

   - A combination of Depth-First Search **(DFS)** where the maximum depth is increased incrementally until a solution is found

   - **Implementation**:
     - Based on textbook implementation (Page 99) with recursive use of **DLS** (Depth Limited Search).

     - **DLS** checks nodes down to the current depth, increasing depth in **IDDFS** if no solution is found

     - Tracks visited nodes in `visited` to avoid revisiting them in the current iteration

   - **Optimality**: Yes, **IDDFS** finds an optimal path if all actions costs are identical 

3. **Greedy Best-First Search (GBFS)** 🏃:

   - A search algorithm focused on moving towards the goal solely on a heuristic value given by a specific heuristic function.
    The next node is chosen based on its proximity to the goal without considering the accumulated cost (which is path-cost + heuristic value)

   - **Implementation**:

     - We use **Euclidean Distance** as the heuristic for the algorithm (explanation on the heuristic could be found in [Heuristics Section](#heuristics-🧠))      

     - Maintains a priority queue `heapq` to manage nodes based on heuristic values, a `reached` set to avoid loops, and a `frontier` list.
     
     - We check nodes from the priority queue, stopping when a goal state is found. If goal is not found, we pick the next node on the priority queue and repeat until goal state is found.

     - If no solution is found, return None

   - **Optimality**: No, **GBFS** doesn't account for path costs, which as a result may find a suboptimal path because it doesn't always explore the best path (it may overlook the more expensive or longer paths that initially look less promising according to the heuristic but are realistically the optimal paths). Therefore, even with an admissible heuristic, **GBFS** won't always find the optimal solution

4. **A*** 🚀:

   - A search algorithm that finds the shortest path from the start state to the goal, using a combination of **Uniform Cost Search** and **Greedy Best-First Search**. The algorithm decides which node to pick using a function f(x) which is the sum of the path-cost g(x) and the heuristic value h(x) from a given heuristic

    - **Implementation**:

      - We use **Linear Conflict** as the heuristic for the algorithm (explanation on the [Heuristics Section](#heuristics-🧠))  

      - The algorithm maintains a priority queue `heapq` to manage nodes based on the f(x) values, a `reached` set to avoid loops, and a `frontier` list

      - We check nodes from the priority queue, stopping when a goal state is found. If goal is not found, we pick the next node on the priority queue and repeat until goal state is found

      - If no solution is found, return None

   - **Optimality**: **A*** will be guaranteed to find the optimal path from the start state to the goal state **only if** the given heuristic is admissible (never overestimates the true cost to reach the goal), the **Euclidean Distance** is admissible, therefore **A*** will find the optimal path    

## Heuristics 🧠   
- Heuristics are used to guide the **Informed Search Algorithms** towards a solution more efficiently. A good heuristic can speed up the search while also potentially find an optimal solution. In the 8-puzzle solver, The **Linear Conflict** and **Euclidean Distance** heuristics were used to implement the **GBFS** and **A*** Algorithms in this project:

1. **Euclidean Distance Heuristic**📐:
   - **Implementation**:
      - Calculate the straight-line distance between a tile's current position and its goal position based on the formula: **sqrt((x2 - x1) ^2 + (y2 - y1)^2 )**
      
      - (x1,x2) is the current position and (x2,y2) is the goal position

   - **Consistency**: The Heuristic is consistent because the estimated distance (which is a straight-line distance) between the current state and a goal state is always less than or equal to the actual cost to move to a neighboring state + the estimated distance from that neighbor to the goal state. It therefore means that there the heuristic doesn't create any overestimations.
   - **Admissibility**: The Heuristic is admissible, it provides the shortest possible path in a straight line to the goal state, so it never overestimates the true cost to reach the goal 


2. **Linear Conflict**📏: 
    - **Implementation**: 
      - An enhancement of the **Manhattan Distance** heuristic

      - Count the number of pairs of tiles within the puzzle matrix that are in **linear conflict**
    
      - Two tiles T1 and T2 are in **Linear Conflict** if: 
        1. T1 and T2 are in the same row/column
      
        2. The goal positions of T1 and T2 are both in that row/column

        3. T1 is to the right of T2, and the goal position of T1 is to the left of the goal position of T2 (**Note:** For columns it is if T1 is lower than T2, and the goal position of T1 is higher than the goal position of T2)

      - Find the **Manhattan Distance** of the given puzzle state

      - Calculate The Linear Conflict heuristic value: **2 * number of pairs that are in Linear Conflict + Manhattan Distance Value**

   
   - **Consistency**: The Heuristic is consistent because it builds on the **Manhattan Distance** (which is consistent) and the addition of conflict penalties doesn't create any overestmiations
  
   - **Admissibility**: The heuristic is admissible because it uses the **Manhattan Distance** which is an admissible heuristic and it adds 2 extra moves for each pair of tiles that are in conflict to resolve the conflict (Therefore, It won't make any overestmiations because it needs at least 2 moves: to move out of the way and to reposition the tile again) 


