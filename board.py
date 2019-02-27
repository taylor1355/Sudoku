import numpy as np
import math

class Board:
    def __init__(self, length, board=None):
        self.length = length

        self.board = board # row, col; current values
        if board is None:
            self.board = np.zeros((length, length), dtype=int)

        # as a simplifying assumption (will change later), assume length is a perfect square
        group_length = int(math.sqrt(length))
        if length <= 0 or group_length ** 2 != length:
            raise ValueError('Length should be a positive perfect square')

        self.groups = np.ones((length, length, length), dtype=int) # group, row, col; masks for where groups are
        for r in range(group_length):
            for c in range(group_length):
                group_num = r * group_length + c
                board_r = r * group_length
                board_c = c * group_length
                self.groups[group_num, board_r : board_r + group_length, board_c : board_c + group_length] = 0

        self.group_index = np.argmin(self.groups, axis=0) # group index at every position

        self.possible = np.ones((length, length, length), dtype=int) # value, row, col; mask for where new values can be placed
        self.calculate_possible()

    # todo: this may be much more efficient using hashmaps rather than np arrays, certainly for large lengths, also by keeping track of non-empty tiles
    def calculate_possible(self):
        for r in range(self.length):
            for c in range(self.length):
                val_index = self.board[r, c] - 1
                if val_index != -1:
                    self.possible[val_index, r, :] = 0
                    self.possible[val_index, :, c] = 0
                    group_index = self.group_index[r, c]
                    self.possible[val_index] *= self.groups[group_index]
