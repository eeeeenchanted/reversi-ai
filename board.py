# -*- coding: utf-8 -*-
from config import *


# 棋盘
class Board:
    def __init__(self):
        self.mtx = []
        self.valid_list = []
        for i in range(row):
            self.mtx.append([])
            for j in range(col):
                self.mtx[i].append(None)
        # 初始化4个棋子
        self.mtx[3][3] = white
        self.mtx[4][4] = white
        self.mtx[3][4] = black
        self.mtx[4][3] = black
        self.cnt = 4
        self.last_move = [None, None]

    # 判断棋盘是否下满
    def is_full(self):
        for i in range(row):
            for j in range(col):
                if self.mtx[i][j] is None:
                    return False
        return True

    def __str__(self):
        return str(self.mtx)
