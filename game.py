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


def init_game_auto(player):
    #root.destroy()
    #root = Tk()
    #chessboard = ChessBoard(root, width=config.frame_width, height=config.frame_height, background='#91989F')
    action_auto = Action_auto(start_game_auto)
    start_game_auto(action_auto, player)


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
    chessboard.bind("<Button-1>", handler_adaptor(on_chessboard_click, action=action))
    chessboard.pack()
    chessboard.draw(board)


def init_game(root, player):
    root.destroy()
    root = Tk()
    chessboard = ChessBoard(root, width=config.frame_width, height=config.frame_height, background='#91989F')
    action = Action(root, chessboard)
    start_game(action, player, chessboard)
    root.focus_set()  # 获得鼠标焦点
    root.wm_title("Reversi")
    root.mainloop()


def start_game_auto(action_auto, player):
    board = Board()
    action_auto.build_board(board, player)
    if player == 0:
        config.state = config.State.human
        board.valid_list = get_valid_list(board.mtx, config.black)
    elif player == 1:
        config.state = config.State.AI
        config.human_color = config.white
        config.AI_color = config.black
        board.valid_list.clear()
        action_auto.ai_play()
