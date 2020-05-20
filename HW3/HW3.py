import numpy as np
np.random.seed(0)
from math import sqrt
from itertools import combinations

ini_safe_ls = []
LEVEL = "easy"

class Minesweeper():
    '''
    game control module
    '''
    def __init__(self, level = "easy"):
        self.level = level
        if self.level == "easy":
            self.width = 9
            self.height = 9
            self.mines = 10
        elif self.level == "medium":
            self.width = 16
            self.height = 16
            self.mines = 25
        elif self.level == "hard":
            self.width = 30
            self.height = 16
            self.mines = 99
        self.ini_safe_num = round(sqrt(self.width * self.height))
        self.gen_board()

    def gen_board(self):
        self.board = np.zeros([self.height, self.width])
        rand_seq = np.random.permutation(self.height * self.width)
        for i in range(self.mines):
            y = rand_seq[i] // self.width
            x = rand_seq[i] % self.width
            self.board[y][x] = 1
        self.ini_safe()

    def hint(self, x, y):
        counter = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if (i < 0 or i >= self.width):
                    continue
                if (j < 0 or j >= self.height):
                    continue
                if (i == x and j == y):
                    continue
                if (self.board[j][i] == 1):
                    counter += 1
        return counter

    def ini_safe(self):
        counter = 0
        i = 0
        rand_seq = np.random.permutation(self.width * self.height)
        while counter < self.ini_safe_num:
            y = rand_seq[i] // self.width
            x = rand_seq[i] % self.width
            if self.board[y][x] == 0:
                ini_safe_ls.append(tuple([(x, y)]))
                counter += 1
            i += 1

    def display(self):
        for j in range(self.height):
            print("----" * self.width)
            for i in range(self.width):
                if (i == 0):
                    print("|", end = "")
                if (self.board[j][i] == 0):
                    print("   ", end = "|")
                elif (self.board[j][i] == 1):
                    print('\033[31m' + " * " + '\x1b[0m', end = "|")
            print("")
        print("----" * self.width)

class Player():
    '''
    player module
    '''
    def __init__(self, game):
        self.KB = dict({i:0 for i in ini_safe_ls})
        self.KB0 = dict()
        self.game = game

        if self.game.level == "easy":
            self.width = 9
            self.height = 9
            self.mines = 10
        elif self.game.level == "medium":
            self.width = 16
            self.height = 16
            self.mines = 25
        elif self.game.level == "hard":
            self.width = 30
            self.height = 16
            self.mines = 99

        self.board = np.full((self.height, self.width), np.inf)

    def play(self):
        single = False
        cell = tuple()
        for key in self.KB.keys():
            if len(key) == 1:
                single = True
                cell = key
                break
        if single == True:
            self.mark(cell)
            self.KB0[cell] = self.KB[cell]
            self.matching(cell)
            self.KB.pop(cell, None)
        else:
            self.matching()

    def mark(self, cell):
        x = cell[0][0]
        y = cell[0][1]
        if (self.KB[cell] == 0):
            self.board[y][x] = self.query(x, y)
            self.gen_clauses(x, y)
        elif (self.KB[cell] == 1):
            self.board[y][x] = -1

    def matching(self, cell = None):
        if (cell == None):
            pass
        else:
            # check duplicate and subsumption
            state = self.KB[cell]
            for key in self.KB.keys():
                if self.KB[key] == state:
                    continue
                else:
                    pass

    def insert(self):
        pass

    def query(self, x, y):
        reply = self.game.hint(x, y)
        return reply

    def gen_clauses(self, x, y):
        mines_cnt = int(self.board[y][x])
        unmark_cnt, unmark_ls = self.cal_unmark(x, y)

        if (mines_cnt == 0):
            for cell in unmark_ls:
                i = cell[0]
                j = cell[1]
                self.KB[tuple([(i, j)])] = 0
        elif (mines_cnt == unmark_cnt):
            for cell in unmark_ls:
                i = cell[0]
                j = cell[1]
                self.KB[tuple([(i, j)])] = 1
        elif (unmark_cnt > mines_cnt):
            combs = list(combinations(unmark_ls, unmark_cnt - mines_cnt + 1))
            for comb in combs:
                ls = []
                for cell in comb:
                    ls.append(cell)
                self.KB[tuple(ls)] = 1


    def cal_unmark(self, x, y):
        num = 0
        ls = []
        for j in range (y-1, y+2):
            for i in range (x-1, x+2):
                if (i < 0 or i >= self.width):
                    continue
                if (j < 0 or j >= self.height):
                    continue
                if (i == x and j == y):
                    continue
                if (self.board[j][i] == np.inf):
                    num += 1
                    ls.append((i, j))
        return num, ls

    def result(self):
        for j in range(self.height):
            print("----" * self.width)
            for i in range(self.width):
                if (i == 0):
                    print("|", end = "")
                if (self.board[j][i] == np.inf):
                    print("   ", end = "|")
                elif (self.board[j][i] == -1):
                    print('\033[31m' + " * " + '\x1b[0m', end = "|")
                else:
                    print(" %d " %self.board[j][i], end = "|")
            print("")
        print("----" * self.width)


if __name__ == "__main__":
    game = Minesweeper(level = LEVEL)
    game.display()
    player = Player(game)
    player.play()
    player.result()

