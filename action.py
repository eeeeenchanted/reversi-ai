from config import *
from mcts import *
from rule import *
from game import *
from tkinter import messagebox
from time import *


class Action:
    def __init__(self, root, canvas, start_game, board):
        self.root = root
        self.canvas = canvas
        self.start_game = start_game
        self.board = board
        self.tree = MCTreeSearch(self.board, black)
        self.total_time = 0

    @staticmethod
    def get_pos(event):
        # print((event.x - left_up_x) // box_width, (event.y - left_up_y) // box_height)
        return (event.x - left_up_x) // box_width, (event.y - left_up_y) // box_height

    def on_click(self, event):
        if state == State.human:
            # print(event)
            if event.x <= 50 and event.y <= 50:
                self.start_game(self, human_color, self.canvas)
            else:
                self.human_play(event)
                self.ai_play()
        pass

    def human_play(self, event):
        x, y = self.get_pos(event)
        # print(x, y)
        valid_list = get_valid_list(self.board.mtx, human_color)
        if len(valid_list) != 0:
            if (x, y) not in valid_list:
                return
            self.board = move(self.board, x, y, human_color)
            self.board.valid_list = []
            self.canvas.draw(self.board)
        else:
            print("no valid place, player pass")
            if self.board.is_full():
                self.finish()
        self.switch_player((x, y))

    def ai_play(self):
        valid_list = get_valid_list(self.board.mtx, AI_color)
        (x, y) = (None, None)
        if len(valid_list) != 0:
            begin = time()
            (x, y) = self.tree.uct_search()
            end = time()
            print('Single step time: ', end - begin)
            self.board = move(self.board, x, y, AI_color)
        else:
            print("no valid place, AI pass")
            if self.board.is_full():
                self.finish()
        self.board.valid_list = get_valid_list(self.board.mtx, human_color)
        self.canvas.draw(self.board)
        if len(self.board.valid_list) == 0:
            print("no valid place, player pass")
            self.tree.update_tree(self.board, AI_color, (x, y), force=True)
            self.ai_play()
        else:
            self.switch_player((x, y))

    def finish(self):
        human = 0
        ai = 0
        for i in range(8):
            for j in range(8):
                if self.board.mtx[i][j] == human_color:
                    human += 1
                else:
                    ai += 1
        if human > ai:
            winner = 'human'
        else:
            winner = 'AI'
        messagebox.showinfo("game over", winner + "win")
        pass

    def switch_player(self, pos):
        if config.state == State.human:
            config.state = State.AI
            color = AI_color
        else:
            config.state = State.human
            color = human_color
        if pos[0] is not None and pos[1] is not None:
            self.tree.update_tree(self.board, color, pos)


