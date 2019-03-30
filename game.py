# -*- coding: utf-8 -*-
from tkinter import *
import config
from board import Board
from chessboard import ChessBoard
from action import Action
from rule import *


def handler_adaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def on_click(event, action):
    action.on_click(event)
    # print(event.x, event.y)


def init_game(root, player):
    root.destroy()
    root = Tk()
    chessboard = ChessBoard(root, width=config.frame_width, height=config.frame_height, background='#91989F')
    board = Board()
    action = Action(root, chessboard, start_game, board)
    start_game(action, player, chessboard, board)
    root.focus_set()  # 获得鼠标焦点
    root.wm_title("Reversi")
    root.mainloop()


def start_game(action, player, chessboard, board):
    if player == 0:
        config.state = config.State.human
        board.valid_list = get_valid_list(board.mtx, config.black)
    else:
        config.state = config.State.AI
        config.human_color = config.white
        config.AI_color = config.black
        board.valid_list.clear()
        action.ai_play()
    chessboard.delete(ALL)
    chessboard.bind("<Button-1>", handler_adaptor(on_click, action=action))
    chessboard.pack()
    chessboard.draw(board)
    print(board)
