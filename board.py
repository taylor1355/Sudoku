import numpy as np
import math

class BoardSpec:
    def __init__(self, length):
        self.length = length

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

class Board:
    def __init__(self, spec, to_copy=None):
        self.spec = spec

        if to_copy is None:
            self.current = np.zeros((spec.length, spec.length), dtype=int) # row, col; current values
            self.possible = np.ones((spec.length, spec.length, spec.length), dtype=int) # value, row, col; mask for where new values can be placed
            self.calculate_possible()
        else:
            self.current = np.copy(to_copy.current)
            self.possible = np.copy(to_copy.possible)

    def mark(self, value, row, col):
        self.current[row, col] = value
        self.update_possible(row, col)

    # todo: this may be much more efficient using hashmaps rather than np arrays, certainly for large lengths, also by keeping track of non-empty tiles
    def calculate_possible(self):
        for r in range(self.spec.length):
            for c in range(self.spec.length):
                self.update_possible(r, c)

    def update_possible(self, row, col):
        val_index = self.current[row, col] - 1
        if val_index != -1:
            self.possible[val_index, row, :] = 0
            self.possible[val_index, :, col] = 0
            self.possible[:, row, col] = 0
            group_index = self.spec.group_index[row, col]
            self.possible[val_index] *= self.spec.groups[group_index]
            self.possible[val_index, row, col] = 1

    def copy(self):
        return Board(self.spec, to_copy=self)
