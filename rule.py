# -*- coding: utf-8 -*-
from copy import deepcopy


# 判断该位置是否是合法位置
def is_valid(mtx, x, y, color):
    if mtx[x][y] is not None:
        return False
    # right direction has reverse color
    if x < 6 and mtx[x+1][y] == 1-color:
        for i in range(x+2, 8):
            if mtx[i][y] == color:
                return True
            if mtx[i][y] is None:
                break
    # left
    if x > 1 and mtx[x-1][y] == 1-color:
        for i in range(x-2, -1, -1):
            if mtx[i][y] == color:
                return True
            if mtx[i][y] is None:
                break
    # down
    if y < 6 and mtx[x][y+1] == 1-color:
        for i in range(y+2, 8):
            if mtx[x][i] == color:
                return True
            if mtx[x][i] is None:
                break
    # up
    if y > 1 and mtx[x][y-1] == 1-color:
        for i in range(y-2, -1, -1):
            if mtx[x][i] == color:
                return True
            if mtx[x][i] is None:
                break
    # down right
    if x < 6 and y < 6 and mtx[x+1][y+1] == 1-color:
        for i in range(2, min(8-x, 8-y)):
            if mtx[x+i][y+i] == color:
                return True
            if mtx[x+i][y+i] is None:
                break
    # up right
    if x < 6 and y > 1 and mtx[x+1][y-1] == 1-color:
        for i in range(2, min(8-x, y+1)):
            if mtx[x+i][y-i] == color:
                return True
            if mtx[x+i][y-i] is None:
                break
    # down left
    if x > 1 and y < 6 and mtx[x-1][y+1] == 1-color:
        for i in range(2, min(8-y, x+1)):
            if mtx[x-i][y+i] == color:
                return True
            if mtx[x-i][y+i] is None:
                break
    # up left
    if x > 1 and y > 1 and mtx[x-1][y-1] == 1-color:
        for i in range(2, min(y+1, x+1)):
            if mtx[x-i][y-i] == color:
                return True
            if mtx[x-i][y-i] is None:
                break
    return False


# 翻转
def reverse(mtx, x, y, color):
    # right direction has reverse color
    if x < 6 and mtx[x+1][y] == 1-color:
        for i in range(x+2, 8):
            if mtx[i][y] == color:
                for j in range(x, i):
                    mtx[j][y] = color
                break
            if mtx[i][y] is None:
                break
    # left
    if x > 1 and mtx[x-1][y] == 1-color:
        for i in range(x-2, -1, -1):
            if mtx[i][y] == color:
                for j in range(i, x):
                    mtx[j][y] = color
                break
            if mtx[i][y] is None:
                break
    # down
    if y < 6 and mtx[x][y+1] == 1-color:
        for i in range(y+2, 8):
            if mtx[x][i] == color:
                for j in range(y, i):
                    mtx[x][j] = color
                break
            if mtx[x][i] is None:
                break
    # up
    if y > 1 and mtx[x][y-1] == 1-color:
        for i in range(y-2, -1, -1):
            if mtx[x][i] == color:
                for j in range(i, y):
                    mtx[x][j] = color
                break
            if mtx[x][i] is None:
                break
    # down right
    if x < 6 and y < 6 and mtx[x+1][y+1] == 1-color:
        for i in range(2, min(8-x, 8-y)):
            if mtx[x+i][y+i] == color:
                for j in range(i):
                    mtx[x+j][y+j] = color
                break
            if mtx[x+i][y+i] is None:
                break
    # up right
    if x < 6 and y > 1 and mtx[x+1][y-1] == 1-color:
        for i in range(2, min(8-x, y+1)):
            if mtx[x+i][y-i] == color:
                for j in range(i):
                    mtx[x+j][y-j] = color
                break
            if mtx[x+i][y-i] is None:
                break
    # down left
    if x > 1 and y < 6 and mtx[x-1][y+1] == 1-color:
        for i in range(2, min(8-y, x+1)):
            if mtx[x-i][y+i] == color:
                for j in range(i):
                    mtx[x-j][y+j] = color
                break
            if mtx[x-i][y+i] is None:
                break
    # up left
    if x > 1 and y > 1 and mtx[x-1][y-1] == 1-color:
        for i in range(2, min(y+1, x+1)):
            if mtx[x-i][y-i] == color:
                for j in range(i):
                    mtx[x-j][y-j] = color
                break
            if mtx[x-i][y-i] is None:
                break
    pass


# 获取合法位置链表
def get_valid_list(mtx, color):
    valid_list = []
    for i in range(8):
        for j in range(8):
            if is_valid(mtx, i, j, color):
                valid_list.append((i, j))
    return valid_list


# 获取优先级最高的位置
def get_priority_valid_list(mtx, table, color=1):
    valid_list = []
    for pos in table:
        for (x, y) in pos:
            if is_valid(mtx, x, y, color):
                valid_list.append((x, y))
        if len(valid_list) > 0:
            break
    return valid_list


# 落子并翻转
def move(board, x, y, color, copy=False):
    if copy:
        new_board = deepcopy(board)  # deepcopy生成一个全新的独立的board
    else:
        new_board = board
    new_board.mtx[x][y] = color
    new_board.cnt = new_board.cnt + 1
    reverse(new_board.mtx, x, y, color)
    return new_board


# score = AI - human
def count_score(mtx, color):
    score = 0
    for i in range(8):
        for j in range(8):
            if mtx[i][j] == color:
                score += 1
            elif mtx[i][j] == 1-color:
                score -= 1
    return score
