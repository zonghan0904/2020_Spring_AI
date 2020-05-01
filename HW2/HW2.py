import sys
import time
import numpy as np

class Minesweeper():
    '''
    an environment to minesweeper
    and to observe the backtrack search w/wo forward checking & heuristic.
    '''
    def __init__(self, fc = False, heur = False):
        try:
            self.argc = len(sys.argv)
            self.size_x = int(sys.argv[1])
            self.size_y = int(sys.argv[2])
            self.mines = int(sys.argv[3])
        except:
            pass

        ls = []

        for i in range(4, self.argc):
            ls.append(int(sys.argv[i]))

        self.board = np.array(ls).reshape(self.size_y, self.size_x)
        self.copy = np.array(self.board, copy = True)
        self.found = False
        self.fc = fc
        self.heur = heur

    def minetest(self, bd, x, y):
        '''
        to test whether a node valid.
        '''
        limit = bd[y][x]
        cnt = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i < 0 or i >= self.size_x):
                    continue
                if (j < 0 or j >= self.size_y):
                    continue
                if (bd[j][i] == -2):
                    cnt += 1
                if (cnt > limit):
                    return False
        if (cnt != limit):
            return False
        else:
            return True

    def countmine(self, bd):
        '''
        to count how many mine overall.
        '''
        count = 0
        for i in range(self.size_x):
            for j in range(self.size_y):
                if (bd[j][i] == -2):
                    count += 1

        return count


    def check(self, bd):
        '''
        to check whether win in the final state.
        '''
        for j in range(self.size_y):
            for i in range(self.size_x):
                if (bd[j][i] >= 0):
                    ret = self.minetest(bd, i, j)
                    if (ret == False):
                        return False
        return True

    def mine3_3(self, bd, x, y):
        '''
        to count how many mines in 3 x 3 grid.
        '''
        cnt = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if (i < 0 or i >= self.size_x):
                    continue
                if (j < 0 or j >= self.size_y):
                    continue
                if (bd[j][i] == -2):
                    cnt += 1

        return cnt

    def constrain3_3(self, bd, x, y):
        '''
        to count how many hints in 3 x 3 grid.
        '''
        cnt = 0
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if (i < 0 or i >= self.size_x):
                    continue
                if (j < 0 or j >= self.size_y):
                    continue
                if (bd[j][i] >= 0):
                    cnt += 1

        return cnt

    def forward_check(self, bd, x, y):
        '''
        forward check.
        '''
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if (i < 0 or i >= self.size_x):
                    continue
                if (j < 0 or j >= self.size_y):
                    continue
                if (bd[j][i] >= 0):
                    cnt = self.mine3_3(bd, i, j)
                    if (cnt > bd[j][i]):
                        return False

        return True

    def count_variable(self, bd):
        '''
        to count how many variable.
        '''
        cnt = 0
        for i in range(self.size_x):
            for j in range(self.size_y):
                if (bd[j][i] == -1):
                    cnt += 1
        return cnt


    def backtrack(self, bd, x, y):
        '''
        backtrack search.
        '''
        if self.found:
            return True
        if (x >= self.size_x or y >= self.size_y):
            ret = self.check(bd)
            if (ret == True and self.countmine(bd) == self.mines):
                self.ans = np.array(bd, copy = True)
                self.found = True
            return

        child = np.array(bd, copy = True)
        if (self.board[y][x] == -1 and self.countmine(bd) < self.mines):
            child[y][x] = -2
            #print(child)
        new_x = (x + 1) % self.size_x
        new_y = y
        if (new_x == 0):
            new_y += 1

        if (new_y < self.size_y and new_x < self.size_x):
            while (self.board[new_y][new_x] != -1):
                new_x = (new_x + 1) % self.size_x
                new_y = new_y
                if (new_x == 0):
                    new_y += 1
                if (new_y >= self.size_y or new_x >= self.size_x):
                    break

        if (self.fc == True):
            ret = self.forward_check(bd, new_x, new_y)
            if (ret == True):
                self.backtrack(child, new_x, new_y)
        elif (self.fc == False):
            self.backtrack(child, new_x, new_y)

        if (self.board[y][x] == -1):
            child[y][x] = -5
            #print(child)
        self.backtrack(child, new_x, new_y)


    def heuristic(self, bd, x, y, var_cnt):
        '''
        heuristic function.
        '''
        if self.found:
            return True
        if (var_cnt == 0):
            ret = self.check(bd)
            if (ret == True and self.countmine(bd) == self.mines):
                self.ans = np.array(bd, copy = True)
                self.found = True
            return

        child = np.array(bd, copy = True)
        if (self.board[y][x] == -1 and self.countmine(bd) < self.mines):
            child[y][x] = -2

        constraints = 0
        new_x = 0
        new_y = 0

        for i in range(self.size_x):
            for j in range(self.size_y):
                if (child[j][i] == -1):
                    cons = self.constrain3_3(bd, i, j)
                    if (cons > constraints):
                        constraints = cons
                        new_x = i
                        new_y = j

        if (self.fc == True):
            ret = self.forward_check(bd, new_x, new_y)
            if (ret == True):
                self.heuristic(child, new_x, new_y, var_cnt - 1)
        elif (self.fc == False):
            self.heuristic(child, new_x, new_y, var_cnt - 1)

        if (self.board[y][x] == -1):
            child[y][x] = -5
        self.heuristic(child, new_x, new_y, var_cnt - 1)

    def INFO(self):
        '''
        to print info.
        '''
        print("\n==================================")
        print("INFO:\n")
        print("Width: %d"%self.size_x)
        print("Height: %d"%self.size_y)
        print("Total mines: %d"%self.mines)
        print("Forward checking: %s"%str(self.fc))
        print("Using heuristic: %s"%str(self.heur))


    def printboard(self):
        '''
        to print solution.
        '''
        print("\n==================================\n")
        print("Sample solution:")
        for j in range(self.size_y):
            print("----" * self.size_x)
            for i in range(self.size_x):
                if (i == 0):
                    print("|", end = "")
                if (self.ans[j][i] == -2):
                    print(" * ", end = "|")
                elif (self.ans[j][i] == -5 or self.ans[j][i] == -1):
                    print(" ~ ", end = "|")
                else:
                    print(" %d "%self.ans[j][i], end = "|")
            print("")
        print("----" * self.size_x)


    def solution(self):
        '''
        to get the solution.
        '''
        if (self.heur == False):
            self.backtrack(self.copy, 0, 0)
        else:
            var_cnt = self.count_variable(self.copy)
            self.heuristic(self.copy, 0, 0, var_cnt)



if __name__ == "__main__":
    minesweeper = Minesweeper(fc = False, heur = False)
    if (minesweeper.argc < 4):
        print("[ERROR] input format error")
        sys.exit(-1)


    if (minesweeper.argc < 4 + minesweeper.size_x * minesweeper.size_y):
        print("[ERROR] board not complete")
        sys.exit(0)

    minesweeper.INFO()

    time1 = time.time()
    minesweeper.solution()
    time2 = time.time()
    elapse = time2 - time1

    try:
        minesweeper.printboard()
    except:
        print("\rno solution")

    print("\nelapsed time: %s (s)"%str(elapse))

