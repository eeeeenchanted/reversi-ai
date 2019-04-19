# -*- coding: utf-8 -*-
from random import choice
from node import *
from math import log, sqrt, fabs
import config
from rule import *
from datetime import *
from copy import deepcopy
from multiprocessing.dummy import Pool


class MCTreeSearch:
    def __init__(self, board, color, **kwargs):
        self.color = color
        self.c = 1.414  # constant in UCT, 根号2
        self.time_limit = timedelta(seconds=10)
        self.max_move = 60
        self.root = Node(board, color, None, None)
        self.moves = 4
        self.start_time = None

    # selection
    def tree_policy(self, node):
        while not node.is_terminal():
            if node.is_fully_expanded():
                value, node = self.best_child(node, self.c)
            else:
                return self.expand(node)
        return node

    @staticmethod
    def expand(node):
        random_choose = choice(node.not_explore_list)
        node.add_child(random_choose[0], random_choose[1])  # x, y
        return node.children[-1]  # last children

    @staticmethod
    def best_child(node, c):
        child_ucb = [1 - child.q / child.n + c * sqrt(log(node.n) / child.n) for child in node.children]  # 要用1-???
        max_ucb = max(child_ucb)
        # print(max_ucb)
        index = child_ucb.index(max_ucb)
        return max_ucb, node.children[index]

    # simulation for expanded node
    def default_policy(self, node):
        now_color = self.color
        board = deepcopy(node.board)
        moves = 0
        while moves + self.moves < 64:
            if moves + self.moves < 56:
                valid_list = get_priority_valid_list(board.mtx, config.roxanne_table, now_color)
                if len(valid_list) == 0:  # pass
                    moves += 1  # 为啥要+1?
                    now_color = 1 - now_color
                    continue
                (x, y) = choice(valid_list)
            else:
                valid_list = get_valid_list(board.mtx, now_color)
                if len(valid_list) == 0:  # pass
                    moves += 1  # 为啥要+1?
                    now_color = 1 - now_color
                    continue
                (x, y) = choice(valid_list)
            board = move(board, x, y, now_color)  # simulation不用deepcopy
            now_color = 1 - now_color
            moves += 1
        return count_score(board.mtx, self.color) > 0

    def backup(self, node, reward):
        while node is not None:
            node.n += 1
            if node.color == self.color:
                node.q += reward
            else:
                node.q += 1 - reward
            node = node.parent

    def uct_search(self):
        self.start_time = datetime.utcnow()
        self.multi_simulation(self.root)
        if len(self.root.children) == 0:
            return None
        win_percent, next_step = self.best_child(self.root, 0)  # ??为啥是0
        print("winning percentage: ", win_percent)
        return next_step.last_move

    def simulation(self, node):  # 多线程？
        while datetime.utcnow() - self.start_time < self.time_limit:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.backup(v, reward)
            if node.is_fully_expanded():
                break

    def multi_simulation(self, node):
        self.time_limit = timedelta(seconds=min(config.single_time_limit, 62 - fabs(34 - self.moves) * 2))  # ???
        while datetime.utcnow() - self.start_time < self.time_limit:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.backup(v, reward)
            if node.is_fully_expanded():
                break
        if len(node.children) == 0:
            return

        pool = Pool(len(node.children))
        pool.map(self.simulation, node.children)
        pool.close()
        pool.join()

    def update_tree(self, board, color, last_move, force=False):  # force: player pass之后ai选择
        # print(last_move)
        flag = False  # explored or not
        for child in self.root.children:
            if child.last_move == last_move:
                if force:
                    self.root.children.remove(child)
                    child = Node(board, color, self.root, last_move)
                    self.root.children.append(child)
                    self.root = child
                else:
                    self.root = child
                flag = True
                break
        if not flag:
            child = Node(board, color, self.root, last_move)
            self.root.children.append(child)
            self.root = child
        self.root.valid_list = get_valid_list(self.root.board.mtx, color)
        self.moves = 0
        for i in range(8):
            for j in range(8):
                if board.mtx[i][j] is not None:
                    self.moves += 1










