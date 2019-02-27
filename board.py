import numpy as np
import math

class Board:
    def __init__(self, length, board=None):
        self.length = length

        self.board = board # row, col; current values
        if board is None:
            self.board = np.zeros((length, length), dtype=int)

        self.groups = np.zeros((length, length, length), dtype=int) # group, row, col; masks for where groups are

        # as a simplifying assumption (will change later), assume length is a perfect square
        group_length = int(math.sqrt(length))
        if length <= 0 or group_length ** 2 != length:
            raise ValueError('Length should be a positive perfect square')

        for r in range(group_length):
            for c in range(group_length):
                board_r = r * group_length
                board_c = c * group_length
                self.groups[r * c, board_r : board_r + group_length, board_c : board_c + group_length] = 1

        self.group_index = np.argmax(self.groups, axis=0) # group index at every position

        self.possible = np.zeros((length, length, length), dtype=int) # value, row, col; mask for where new values can be placed
        self.calculate_possible()

    # todo: this may be much more efficient using hashmapsrather than np arrays, certainly for large lengths
    def calculate_possible(self):
        for r in range(self.length):
            for c in range(self.length):
                val = self.board[r, c]
                if val != 0:
                    self.possible[val - 1, r, :] = 0
                    self.possible[val - 1, :, c] = 0
                    self.possible[val - 1][self.groups[val]] = 0
