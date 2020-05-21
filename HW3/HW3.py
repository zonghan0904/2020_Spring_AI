import numpy as np
#np.random.seed(0)
from math import sqrt
from itertools import combinations
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--level", "-L", type = str, default = "easy")
parser.add_argument("--display", "-D", action = "store_true")
args = parser.parse_args()

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
        #self.ini_safe_num = self.width * self.height / 2
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
        self.endgame = False

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

        self.board = np.full((self.height, self.width), -10)

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
            self.gen_clauses(cell[0][0], cell[0][1])
            self.KB.pop(cell, None)
        else:
            self.endgame = True
            self.matching()

    def mark(self, cell):
        x = cell[0][0]
        y = cell[0][1]
        if (self.KB[cell] == 0):
            self.board[y][x] = self.query(x, y)
        elif (self.KB[cell] == 1):
            self.board[y][x] = -1

    def clean_subsumption(self):
        pop_ls = []
        for key in self.KB.keys():
            for other in self.KB.keys():
                if (key == other):
                    continue
                if (set(key).issubset(set(other))) and (self.KB[key] == self.KB[other]):
                    pop_ls.append(other)
        for key in pop_ls:
            self.KB.pop(key, None)

    def matching(self, cell = None):
        self.clean_subsumption()
        if (cell == None):
            for key in self.KB.keys():
                if (len(key) > 2):
                    continue
                state = self.KB[key]
                for other in self.KB.keys():
                    if (key == other):
                        continue
                    if (set(key).issubset(set(other))):
                       pass

        else:
            state = self.KB[cell]
            pop_ls = []
            new_key = []

            for key in self.KB.keys():
                if key == cell:
                    continue
                if (state == 0):
                    if (cell[0] in set(key)) and (self.KB[key] == 1):
                        temp = list(key)
                        temp.remove(cell[0])
                        pop_ls.append(key)
                        new_key.append(temp)
                elif (state == 1):
                    if (cell[0] in set(key)) and (self.KB[key] == 1):
                        pop_ls.append(key)

            for key in pop_ls:
                self.KB.pop(key, None)
            for key in new_key:
                self.KB[tuple(key)] = 1

    def query(self, x, y):
        reply = self.game.hint(x, y)
        return reply

    def gen_clauses(self, x, y):
        mines_cnt = self.board[y][x]
        unmark_cnt, unmark_ls = self.cal_unmark(x, y)
        known_mines = self.cal_mines(x, y)
        mines_cnt -= known_mines

        if (mines_cnt >= 0):
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

    def cal_mines(self, x, y):
        num = 0
        for j in range (y-1, y+2):
            for i in range (x-1, x+2):
                if (i < 0 or i >= self.width):
                    continue
                if (j < 0 or j >= self.height):
                    continue
                if (i == x and j == y):
                    continue
                if (self.board[j][i] == -1):
                    num += 1
        return num

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
                if (self.board[j][i] == -10):
                    num += 1
                    ls.append((i, j))
        return num, ls

    def display(self):
        for j in range(self.height):
            print("----" * self.width)
            for i in range(self.width):
                if (i == 0):
                    print("|", end = "")
                if (self.board[j][i] == -10):
                    print("   ", end = "|")
                elif (self.board[j][i] == -1):
                    print('\033[31m' + " * " + '\x1b[0m', end = "|")
                else:
                    print(" %d " %self.board[j][i], end = "|")
            print("")
        print("----" * self.width)

    def global_constraint(self):
        count = 0
        for j in range(self.height):
            for i in range(self.width):
                if (self.board[j][i] == -1):
                    count += 1
        if (count == self.mines):
            for j in range(self.height):
                for i in range(self.width):
                    if (self.board[j][i] == -10):
                        self.board[j][i] = self.query(i, j)

    def check_residual(self):
        for j in range(self.height):
            for i in range(self.width):
                unmark_cnt, unmark_ls = self.cal_unmark(i, j)
                if (unmark_cnt > 0):
                    mines_cnt = self.board[j][i]
                    known_mines = self.cal_mines(i, j)
                    mines_cnt -= known_mines
                    if (mines_cnt >= 0):
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

    def retry(self):
        self.endgame = False
        self.KB.clear()
        self.check_residual()
        self.play()

    def result(self):
        for j in range(self.height):
            for i in range(self.width):
                if (self.board[j][i] == -10):
                    return False
        return True


if __name__ == "__main__":
    game = Minesweeper(level = args.level)
    player = Player(game)

    while (player.endgame != True):
        player.play()
        if (player.endgame == True):
            player.retry()
    player.global_constraint()
    result = player.result()
    print("success: " + str(result))

    if (args.display):
        game.display()
        player.display()
