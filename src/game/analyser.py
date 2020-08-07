from game.board import Board
from typing import List
from game.notch import Notch


class BoardAnalyser:
    def __init__(self, board: Board):
        self.__board = board
        self.__is_over = False
        self.__winner = None

    def get_full_size(self):
        return self.__board.get_size() * self.__board.get_block_size()

    def get_notch_array(self) -> List[List[Notch]]:
        n = self.__board.get_block_size() * self.__board.get_size()
        return [self.get_notch_row(row_num) for row_num in range(n)]

    def get_notch_row(self, row_num) -> List[Notch]:
        block_size = self.__board.get_block_size()
        block_row = row_num // block_size
        marble_row_on_block = row_num % block_size
        return [notch for block in self.__board.get_blocks()[block_row] for notch in block.get_row(marble_row_on_block)]

    def check_win(self, colours: List[int], win_length) -> None:
        for colour in colours:
            if self.__check_win(colour, win_length):
                self.__is_over = True
                self.__winner = colour
                return

    def get_winner(self):
        return self.__winner

    def __check_win(self, colour: int, win_length: int):
        return any([
            self.__check_vertical_win(colour, win_length),
            self.__check_diagonal_win(colour, win_length),
            self.__check_horizontal_win(colour, win_length)
        ])

    # Check win helpers
    def __check_vertical_win(self, colour: int, win_length: int):
        for col in range(self.get_full_size()):
            for i in range(self.get_full_size() - win_length):
                if all([self.get_notch_array()[row+i][col].colour() == colour for row in range(win_length)]):
                    return True
        return False

    def __check_horizontal_win(self, colour, win_length: int):
        for row in range(self.get_full_size()):
            for i in range(self.get_full_size() - win_length):
                if all([self.get_notch_array()[row][col+i].colour() == colour for col in range(win_length)]):
                    return True
        return False

    def __check_diagonal_win(self, colour, win_length: int):
        n = self.get_full_size()
        w = win_length
        for r_shift in range(n - w):
            for c_shift in range(n - w):
                if any([
                    all([self.get_notch_array()[r_shift+i][c_shift+i].colour() == colour for i in range(w)]),
                    all([self.get_notch_array()[n-r_shift-i-1][n-c_shift-i-1].colour() == colour for i in range(w)])
                ]):
                    return True
        return False