# -*- coding: utf-8 -*-
from rule import *


# 节点
class Node:
    def __init__(self, board, color, parent, last_move):
        self.board = board
        self.color = color
        self.parent = parent
        self.last_move = last_move
        self.children = []
        self.depth = 0
        self.valid_list = get_valid_list(board.mtx, color)
        self.not_explore_list = self.valid_list
        self.n = 0  # visit count
        self.q = 0  # reward

    # 添加子节点
    def add_child(self, x, y):
        new_board = move(self.board, x, y, self.color, copy=True)
        self.children.append(Node(new_board, 1-self.color, self, (x, y)))
        self.not_explore_list.remove((x, y))

    # 是否完全扩展
    def is_fully_expanded(self):
        return len(self.not_explore_list) == 0

    # 是否是终止节点
    def is_terminal(self):
        return len(self.valid_list) == 0 and len(self.children) == 0
