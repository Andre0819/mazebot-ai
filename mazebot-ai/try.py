import math


def print_explored(maze,result):
    print("Optimal Path: ")
    optimal = result[0]
    traversed = result[1]
    # for x in traversed:
    #     if maze[x[0]][x[1]] != 'S' and maze[x[0]][x[1]] != 'G':
    #         maze[x[0]][x[1]] = 'x'

    for x in optimal:
        if maze[x[0]][x[1]] != 'S' and maze[x[0]][x[1]] != 'G':
            maze[x[0]][x[1]] = '*'

    for l in maze:
        for item in l:
            print(item, end='')
        print()

def read_maze():
    with open('mazes/maze5x5.txt', 'r') as f:
        maze_size = int(f.readline())
        squares = [[0 for j in range(maze_size)] for i in range(maze_size)]
        for i in range(maze_size):
            string = f.readline()
            for j in range(maze_size):
                if string[j] == ".":
                    squares[i][j] = 0
                elif string[j] == "#":
                    squares[i][j] = 1
                else:
                    squares[i][j] = string[j]

    return squares

def main():
    2**(63+63)
    return 2 ** (abs(node[0] - goal[0]) + abs(node[1] - goal[1]))





main()
