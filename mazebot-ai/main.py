import heapq
import math
import time
import pygame
from collections import OrderedDict


# The draw_maze function takes in a 'screen' object, the 'maze' (a 2D list), and the block_size (the size of each
# cell in the maze). It then draws the maze using rectangles and different colors based on the character in the maze
# list.
def draw_maze(screen, maze, block_size):
    # define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (75, 75, 75)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    LIGHTORANGE = (200, 200, 100)

    # draw maze as a grid
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            rect = pygame.Rect(j * block_size, i * block_size, block_size, block_size)
            if maze[i][j] == '#':  # wall
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
            elif maze[i][j] == 'S':  # start
                pygame.draw.rect(screen, YELLOW, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
            elif maze[i][j] == 'G':  # goal
                pygame.draw.rect(screen, GREEN, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
            elif maze[i][j] == 'x':  # traversed
                pygame.draw.rect(screen, LIGHTORANGE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
            elif maze[i][j] == '*':  # optimal path
                pygame.draw.rect(screen, ORANGE, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
            else:  # unexplored
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)


# The print_explored_gui function initializes the Pygame screen, calls the draw_maze function to draw the initial maze,
# and then draws the search path by updating the maze list with 'x' characters for the traversed path and '*' characters
# for the optimal path. It then sleeps for a short duration and updates the screen to visualize the search path.
def print_explored_gui(maze, result):
    # initialize Pygame
    pygame.init()

    # set up screen
    block_size = 50 // (len(maze) / 10)
    width = len(maze[0]) * block_size
    height = len(maze) * block_size
    screen = pygame.display.set_mode((width + 300, height))
    pygame.display.set_caption("Maze Solver")

    font = pygame.font.SysFont('Arial', 23)

    def screenmessage(msg, color, textheight):
        screen_text = font.render(msg, True, color)
        screen.blit(screen_text, (width, textheight))

    # draw initial maze
    draw_maze(screen, maze, block_size)

    # draw search path
    traversed = result[1]
    for x in traversed:
        if maze[x[0]][x[1]] != 'S' and maze[x[0]][x[1]] != 'G':
            maze[x[0]][x[1]] = 'x'

        draw_maze(screen, maze, block_size)
        pygame.display.update()
        time.sleep(0.02)
    if result[0] is not None:
        # draw search path
        optimal = result[0]
        # draw optimal path
        for x in optimal:
            if maze[x[0]][x[1]] != 'S' and maze[x[0]][x[1]] != 'G':
                maze[x[0]][x[1]] = '*'

            draw_maze(screen, maze, block_size)
            pygame.display.update()
            time.sleep(0.03)

    # wait for user to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screenmessage("Maze size: " + str(len(maze)) + "x" + str(len(maze)), (255, 255, 255), 0)
        screenmessage("Optimal Path Length: " + (str(len(result[0]) - 2) if result[0] is not None else "No solution"),
                      (255, 255, 255), 30)
        screenmessage("Traversed Path Length: " + str(len(result[1]) - 1), (255, 255, 255), 60)
        pygame.display.update()

    pygame.quit()


# It initializes the frontier as a priority queue with the start node, and the visited and cost as an ordered
# dictionary and dictionary respectively. It then iterates through the nodes in the frontier, adding them to the
# visited set and exploring their neighbors. If the goal node is found, it returns the path and visited set. Else,
# it continues iterating through the frontier until it is empty.
def search(maze, start, goal):
    # initialize frontier, visited set, and cost dictionary
    frontier = []
    visited = OrderedDict()
    cost = {}

    # add start node to the frontier with a priority value of 0
    heapq.heappush(frontier, (0, 0, start))
    cost[start] = (0, None)

    for i in range(len(maze)):
        for j in range(len(maze)):
            if (i, j) != start:
                cost[(i, j)] = (math.inf, None)

    while frontier:
        _, _, current = heapq.heappop(frontier)

        # check if the current node is the goal node
        if current == goal:
            # return the path and visited set
            path = []
            while current in cost:
                path.append(current)
                current = cost[current][1]
            return list(path), list(visited)

        # add the current node to the visited set
        visited[current] = None

        # explore the neighbors of the current node
        for neighbor in get_neighbors(maze, current):
            # calculate the tentative actual cost to reach the neighbor node
            tentative_cost = cost[current][0] + 1  # assuming each move has a cost of 1

            if tentative_cost < cost[neighbor][0]:
                # update the actual cost and parent node for the neighbor node
                cost[neighbor] = (tentative_cost, current)
                hscore = heuristic(neighbor, goal)
                priority = tentative_cost + hscore
                # add the neighbor node to the frontier with the priority value
                heapq.heappush(frontier, (priority, hscore, neighbor))

    # if the frontier is empty and the goal node has not been found, return None
    return None, visited


# UI
def get_neighbors(maze, node):
    # get the row and column of the current node
    row, col = node

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # check each possible move and add valid neighbors to the list
    neighbors = []
    for move in moves:
        new_row = row + move[0]
        new_col = col + move[1]
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == '.':
            neighbors.append((new_row, new_col))

    return neighbors


# The heuristic function simply returns the manhattan distance
def heuristic(node, goal):
    # heuristic just manhattan
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


# Reads a text file that contains the maze to be sued by the bot and the A* algorithm
def read_maze():
    # Modify the string below to the file name including the .txt extension
    file = 'mazes/wide_maze_2.txt'  # change this string

    # Open file and create a 2d list representing the maze
    with open(file, 'r') as f:
        maze_size = int(f.readline())
        squares = [[0 for j in range(maze_size)] for i in range(maze_size)]
        for i in range(maze_size):
            string = f.readline()
            for j in range(maze_size):
                squares[i][j] = string[j]

    return squares


# Actual main function
def main():
    # read txt file and print 2d maze grid
    maze = read_maze()
    print(len(maze))
    for i in maze:
        for item in i:
            print(item, end='')
        print()

    # get initial state index
    start_index = [(i, j) for i, row in enumerate(maze) for j, val in enumerate(row) if val == 'S']

    # get goal state index
    end_index = [(i, j) for i, row in enumerate(maze) for j, val in enumerate(row) if val == 'G']

    # replace the characters with '.' after getting indexes
    maze[start_index[0][0]][start_index[0][1]] = '.'
    maze[end_index[0][0]][end_index[0][1]] = '.'

    # print out the path traveled
    result = search(maze, start_index[0], end_index[0])

    # bring back S and G
    maze[start_index[0][0]][start_index[0][1]] = 'S'
    maze[end_index[0][0]][end_index[0][1]] = 'G'

    # printing the maze
    print_explored_gui(maze, result)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
