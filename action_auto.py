# -*- coding: utf-8 -*-
from mcts import *
from game import *
from tkinter import messagebox
from time import *
import pickle
from chessboard import *
from config import *
from rule import *

'''
实现自博弈的代码，不过最后没有成功
'''

class Action_auto:
    def __init__(self, start_game):
        self.start_game = start_game
        self.total_time = 0
        self.board = None
        self.tree = None

    def on_click(self, event):
        if config.state == State.human:
            print(event)
            self.human_play(event)
            self.ai_play()
        pass

    def autoplay(self):
        if config.state == State.human:
            self.ai_play_2()
            self.ai_play()
        pass

    @staticmethod
    def get_pos(event):
        # print((event.x - left_up_x) // box_width, (event.y - left_up_y) // box_height)
        return (event.x - left_up_x) // box_width, (event.y - left_up_y) // box_height

    def human_play(self, event):
        x, y = self.get_pos(event)
        # print(x, y)
        valid_list = get_valid_list(self.board.mtx, config.human_color)
        if len(valid_list) != 0:
            if (x, y) not in valid_list:
                print(x, y, "can't click here")
                return
            print(x, y)
            move(self.board, x, y, config.human_color)  # reconsider
            self.board.valid_list = []
            self.board.last_move = [x, y]
        else:
            print("no valid place, player pass")
            if self.board.is_full():
                self.finish()
                return
        self.switch_player((x, y))

    def ai_play(self):
        if config.state == State.human:
            return
        # print(config.AI_color)
        valid_list = get_valid_list(self.board.mtx, config.AI_color)
        (x, y) = (None, None)
        if len(valid_list) != 0:
            begin = time()
            (x, y) = self.tree.uct_search()
            end = time()
            print('Single step time: ', end - begin)
            self.total_time = self.total_time+end - begin
            self.board = move(self.board, x, y, config.AI_color)
            passAI = FALSE
        else:
            print("no valid place, AI pass")
            passAI = TRUE
            if self.board.is_full():
                self.finish()
                return
        self.board.valid_list = get_valid_list(self.board.mtx, config.human_color)
        self.board.last_move = [x, y]
        if len(self.board.valid_list) == 0:
            print("no valid place, player pass")
            if passAI:
                self.finish()
                return
            self.tree.update_tree(self.board, config.AI_color, (x, y), force=True)  # ?
            self.ai_play()
        else:
            self.switch_player((x, y))
        self.autoplay()

    def ai_play_2(self):
        # print(config.AI_color)
        valid_list = get_valid_list(self.board.mtx, config.human_color)
        self.tree.root.valid_list = get_valid_list(self.tree.root.board.mtx, config.human_color)
        (x, y) = (None, None)
        # print("valid list")
        # print(len(valid_list))
        if len(valid_list) != 0:
            #begin = time()
            (x, y) = self.tree.uct_search()
            #end = time()
            #print('Single step time: ', end - begin)
            #self.total_time = self.total_time+end - begin
            self.board = move(self.board, x, y, config.human_color)
            self.board.valid_list = []
            self.board.last_move = [x, y]
        else:
            #print("no valid place, AI2 pass")
            if self.board.is_full():
                self.finish()
                return
        self.switch_player((x, y))

    def finish(self):
        human = 0
        ai = 0
        for i in range(8):
            for j in range(8):
                if self.board.mtx[i][j] == config.human_color:
                    human += 1
                else:
                    ai += 1
        if human > ai:
            winner = 'human'
        else:
            winner = 'AI'
        # messagebox.showinfo("game over", winner + " win")
        config.count = config.count+1
        config.state = State.finished
        print('total time', self.total_time)
        while self.tree.root.parent is not None:
            self.tree.root = self.tree.root.parent
        self.write(config.parameter, self.tree)  # save tree structure into file
        # config.player_now = 1-config.player_now
        self.start_game(self, config.player_now)
        print(config.count)

    def switch_player(self, pos):
        if config.state == State.human:
            config.state = State.AI
            color = config.AI_color
        else:
            config.state = State.human
            color = config.human_color
        if pos[0] is not None and pos[1] is not None:
            self.tree.update_tree(self.board, color, pos)

    def build_board(self, board, player):
        self.board = board
        if self.tree is not None:
            while self.tree.root.parent is not None:
                self.tree.root = self.tree.root.parent
        else:
            self.tree = self.build_tree(player)

    def build_tree(self, player):
        if player == 0:
            config.parameter = 'player_first'
        else:
            config.parameter = 'AI_first'
        try:
            tree = self.read(config.parameter)  # read previous trained tree
            while tree.root.parent is not None:
                tree.root = tree.root.parent
        except FileNotFoundError:
            self.write(config.parameter)
            tree = self.read(config.parameter)
        return tree

    @staticmethod
    def read(filename):
        with open(filename, 'rb') as f:
            aa = pickle.load(f)
            print(aa)
            return aa

    def write(self, filename, t=None):
        with open(filename, 'wb') as f:
            if t is None:
                t = MCTreeSearch(self.board, black)
            pickle.dump(t, f)
