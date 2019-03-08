import numpy as np
import math

# using forward checking
def solve(board):
    num_possibilities = np.sum(board.possible, axis=0)
    flat_indices = np.argsort(num_possibilities, axis=None) # todo: find min subject to not already filled out constraint instead of sorting

    # print(board.current)
    # print(num_possibilities)

    length = board.spec.length
    for i in range(len(flat_indices)):
        index = flat_indices[i]
        if num_possibilities.flat[index] == 0: # backtrack
            return None
        elif board.current.flat[index] == 0: # variable not already assigned
            for value in range(1, length + 1):
                if board.possible[value - 1].flat[index]:
                    row, col = index // length, index % length
                    board_copy = board.copy()
                    board_copy.mark(value, row, col)
                    solution = solve(board_copy)
                    if solution is not None:
                        return solution
            return None
    return board
