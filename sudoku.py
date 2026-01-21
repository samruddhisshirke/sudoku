import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit,
    QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from copy import deepcopy


class Sudoku(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("\U0001F9E9 Sudoku Game")
        self.setStyleSheet("background-color: #f5f5f5;")
        self.setFixedSize(620, 740)

        self.grid = [[None for _ in range(9)] for _ in range(9)]
        self.solution = [[0]*9 for _ in range(9)]
        self.puzzle = [[0]*9 for _ in range(9)]

        self.initUI()
        self.generate_puzzle()

    def initUI(self):
        main_layout = QVBoxLayout()

        title = QLabel("Sudoku")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #444;")
        main_layout.addWidget(title)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)

        for row in range(9):
            for col in range(9):
                cell = QLineEdit()
                cell.setMaxLength(1)
                cell.setAlignment(Qt.AlignCenter)
                cell.setFont(QFont("Courier", 18))
                cell.setFixedSize(55, 55)
                cell.setStyleSheet(self.cell_border_style(row, col))
                cell.returnPressed.connect(self.check_cell)
                self.grid[row][col] = cell
                grid_layout.addWidget(cell, row, col)

        button_layout = QHBoxLayout()
        hint_btn = QPushButton("\U0001F4A1 Hint")
        reset_btn = QPushButton("\U0001F504 Reset")
        new_btn = QPushButton("\U0001F195 New")

        for btn in (hint_btn, reset_btn, new_btn):
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            btn.setFixedWidth(120)

        hint_btn.clicked.connect(self.give_hint)
        reset_btn.clicked.connect(self.reset_board)
        new_btn.clicked.connect(self.generate_puzzle)

        button_layout.addWidget(hint_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(new_btn)

        main_layout.addLayout(grid_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def cell_border_style(self, row, col):
        style = "QLineEdit { background-color: white; color: black; border: 1px solid #ccc;"

        if row == 0:
            style += "border-top: 3px solid black;"
        if row == 8:
            style += "border-bottom: 3px solid black;"
        if col == 0:
            style += "border-left: 3px solid black;"
        if col == 8:
            style += "border-right: 3px solid black;"

        if row in [3, 6]:
            style += "border-top: 2px solid black;"
        if col in [3, 6]:
            style += "border-left: 2px solid black;"

        style += " border-radius: 4px; }"
        return style

    def generate_puzzle(self):
        self.solution = self.generate_complete_board()
        self.puzzle = deepcopy(self.solution)

        for box_row in range(3):
            for box_col in range(3):
                nums = [(r, c) for r in range(box_row*3, box_row*3+3)
                                 for c in range(box_col*3, box_col*3+3)]
                random.shuffle(nums)
                to_keep = random.randint(3, 4)
                keep = nums[:to_keep]
                for r, c in nums:
                    if (r, c) not in keep:
                        self.puzzle[r][c] = 0

        for r in range(9):
            for c in range(9):
                val = self.puzzle[r][c]
                cell = self.grid[r][c]
                cell.setText(str(val) if val else "")
                if val != 0:
                    cell.setReadOnly(True)
                    cell.setStyleSheet("background-color: #e0f7fa; color: blue; font-weight: bold;" + self.border_addition(r, c))
                else:
                    cell.setReadOnly(False)
                    cell.setStyleSheet(self.cell_border_style(r, c))

    def reset_board(self):
        for r in range(9):
            for c in range(9):
                val = self.puzzle[r][c]
                cell = self.grid[r][c]
                cell.setText(str(val) if val else "")
                if val != 0:
                    cell.setReadOnly(True)
                    cell.setStyleSheet("background-color: #e0f7fa; color: blue; font-weight: bold;" + self.border_addition(r, c))
                else:
                    cell.setReadOnly(False)
                    cell.setStyleSheet(self.cell_border_style(r, c))

    def border_addition(self, row, col):
        style = ""
        if row == 0:
            style += "border-top: 3px solid black;"
        if row == 8:
            style += "border-bottom: 3px solid black;"
        if col == 0:
            style += "border-left: 3px solid black;"
        if col == 8:
            style += "border-right: 3px solid black;"
        if row in [3, 6]:
            style += "border-top: 2px solid black;"
        if col in [3, 6]:
            style += "border-left: 2px solid black;"
        return style

    def generate_complete_board(self):
        def is_safe(board, row, col, num):
            for x in range(9):
                if board[row][x] == num or board[x][col] == num:
                    return False
            start_row, start_col = 3 * (row//3), 3 * (col//3)
            for i in range(3):
                for j in range(3):
                    if board[start_row+i][start_col+j] == num:
                        return False
            return True

        def solve_board(board):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if is_safe(board, i, j, num):
                                board[i][j] = num
                                if solve_board(board):
                                    return True
                                board[i][j] = 0
                        return False
            return True

        board = [[0]*9 for _ in range(9)]
        solve_board(board)
        return board

    def check_cell(self):
        complete = True
        for row in range(9):
            for col in range(9):
                cell = self.grid[row][col]
                val = cell.text().strip()
                if self.puzzle[row][col] != 0:
                    continue
                if val.isdigit():
                    if int(val) == self.solution[row][col]:
                        cell.setStyleSheet("background-color: #c8e6c9; color: green; font-weight: bold;" + self.border_addition(row, col))
                    else:
                        cell.setStyleSheet("background-color: #ffcdd2; color: red; font-weight: bold;" + self.border_addition(row, col))
                        complete = False
                else:
                    complete = False
                    cell.setStyleSheet("background-color: #ffcdd2; color: red; font-weight: bold;" + self.border_addition(row, col))

        if complete:
            QMessageBox.information(self, "\U0001F389 Sudoku Solved", "\U0001F389 Congratulations! You solved the Sudoku!")

    def give_hint(self):
        empty_cells = [
            (r, c) for r in range(9) for c in range(9)
            if self.grid[r][c].text() == ""
        ]
        if not empty_cells:
            QMessageBox.information(self, "Hint", "No more hints available.")
            return

        r, c = random.choice(empty_cells)
        self.grid[r][c].setText(str(self.solution[r][c]))
        self.grid[r][c].setStyleSheet("background-color: #d0ffd0; color: darkgreen; font-weight: bold;" + self.border_addition(r, c))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Sudoku()
    window.show()
    sys.exit(app.exec_())
