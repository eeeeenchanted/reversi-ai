# -*- coding: utf-8 -*-
from tkinter import *
import config
from board import Board
from chessboard import ChessBoard
from action import Action
from action_auto import Action_auto
from rule import *


def handler_adaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def on_chessboard_click(event, action):
    action.on_click(event)

    pass


# 初始化游戏
def init_game(root, player):
    root.destroy()
    root = Tk()
    chessboard = ChessBoard(root, width=config.frame_width, height=config.frame_height, background='#91989F')
    action = Action(root, chessboard)
    start_game(action, player, chessboard)
    root.focus_set()  # 获得鼠标焦点
    root.wm_title("Reversi")
    root.mainloop()  # 游戏主循环


# 开始游戏
def start_game(action, player, chessboard):
    board = Board()
    action.build_board(board, player)
    if player == 0:
        config.state = config.State.human
        board.valid_list = get_valid_list(board.mtx, config.black)
    elif player == 1:
        config.state = config.State.AI
        config.human_color = config.white
        config.AI_color = config.black
        board.valid_list.clear()
        action.ai_play()
    chessboard.delete(ALL)
    # 棋盘绑定鼠标左键，获取鼠标点击事件
    chessboard.bind("<Button-1>", handler_adaptor(on_chessboard_click, action=action))
    chessboard.pack()
    chessboard.draw(board)  # 绘制棋盘


