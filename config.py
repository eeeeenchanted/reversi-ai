# -*- coding: utf-8 -*-
from enum import Enum


class State(Enum):
    human = 1
    AI = 2
    finished = 3
    start = 4


state = State.start
human_color = 0
AI_color = 1
parameter = "player_first"
row = 8
col = 8
black = 0
white = 1
box_width = 50
box_height = 50
chess_radius = 22
next_radius = 10
next_color = "#BDC0BA"
left_up_x = 50
left_up_y = 50
right_down_x = left_up_x + box_width * row
right_down_y = left_up_y + box_height * col
first_chess_x = left_up_x + box_width / 2
first_chess_y = left_up_y + box_height / 2
line_color = "#111"
bg_color = "#81C7D4"
last_move_color = "#1E88A8"
last_move_radius = 7
frame_width = 500
frame_height = 500
time_limit = 60
single_time_limit = 3

roxanne_table = [[(0, 0), (0, 7), (7, 0), (7, 7)],
                 [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3), (3, 4), (3, 5),
                  (4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)],
                 [(2, 0), (3, 0), (4, 0), (5, 0), (2, 7), (3, 7), (4, 7), (5, 7),
                  (0, 2), (0, 3), (0, 4), (0, 5), (7, 2), (7, 3), (7, 4), (7, 5)],
                 [(2, 1), (3, 1), (4, 1), (5, 1), (2, 6), (3, 6), (4, 6), (5, 6),
                  (1, 2), (1, 3), (1, 4), (1, 5), (6, 2), (6, 3), (6, 4), (6, 5)],
                 [(0, 1), (1, 0), (1, 1), (1, 6), (0, 6), (1, 7),
                  (6, 1), (6, 0), (7, 1), (6, 6), (6, 7), (7, 6)]]
