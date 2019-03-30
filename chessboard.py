# -*- coding: utf-8 -*-
from tkinter import *
from config import *


class ChessBoard(Canvas):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

    def draw(self, board):
        self.create_rectangle(left_up_x, left_up_y,
                              right_down_x, right_down_y,
                              fill=bg_color, outline=line_color)

        for i in range(row-1):
            delta = left_up_y + box_height*(i+1)
            self.create_line(left_up_x, delta, right_down_x, delta, fill=line_color)
            self.create_line(delta, left_up_y, delta, right_down_y, fill=line_color)

        for i in range(row):
            for j in range(col):
                if board.mtx[i][j] is not None:
                    color = None
                    if board.mtx[i][j] == black:
                        color = 'black'
                    elif board.mtx[i][j] == white:
                        color = 'white'
                    self.create_oval(first_chess_x + box_width * i - chess_radius,
                                     first_chess_y + box_height * i - chess_radius,
                                     first_chess_x + box_width * i + chess_radius,
                                     first_chess_y + box_height * i + chess_radius,
                                     fill=color)

        for pos in board.valid_list:
            self.create_oval(first_chess_x + box_width * pos[0] - next_radius,
                             first_chess_y + box_height * pos[1] - next_radius,
                             first_chess_x + box_width * pos[0] + next_radius,
                             first_chess_y + box_height * pos[1] + next_radius,
                             fill=next_color)

        self.update()

