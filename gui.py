from PySide2 import QtWidgets, QtCore, QtGui
# from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout
# from PySide2.QtCore import Slot, Qt, QSize
# from PySide2.QtGui import QSizePolicy
import sys

from board import Board, BoardSpec

class BoardWindow(QtWidgets.QWidget):
    def __init__(self, board):
        QtWidgets.QWidget.__init__(self)
        self.board = board

        self.board_grid = self.make_board()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.board_grid)
        self.setLayout(self.layout)

    def make_board(self):
        rows, cols = self.board.current.shape
        grid = QtWidgets.QGridLayout(self)
        for row in range(rows):
            for col in range(cols):
                text = str(self.board.current[row, col])
                if text == '0': text = ''
                button = SquareButton(text)
                button.clicked.connect(self.tile_clicked(row, col))
                grid.addWidget(button, row, col)
        return grid

    def tile_clicked(self, row, col):
        def handler():
            val = 1
            self.board.mark(val, row, col)
            self.board_grid.itemAtPosition(row, col).widget().setText(str(val))
            QtWidgets.QApplication.processEvents()
        return handler

class SquareButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def resizeEvent(self, event):
        new_size = QtCore.QSize(1, 1)
        new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
        self.resize(new_size)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    board_spec = BoardSpec(9)
    board = Board(board_spec)

    import numpy as np
    board_init = np.zeros((9, 9), dtype=int)
    for c in range(9):
        board_init[c, c] = c + 1
    board.current = board_init
    board.calculate_possible()

    widget = BoardWindow(board)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
