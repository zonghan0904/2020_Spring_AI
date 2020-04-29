import sys
import time
import numpy as np

argc = len(sys.argv)

if (argc < 4):
    print("[ERROR] input format error")
    sys.exit(-1)

size_x = int(sys.argv[1])
size_y = int(sys.argv[2])
mines = int(sys.argv[3])

if (argc < 4 + size_x * size_y):
    print("[ERROR] board not complete")
    sys.exit(0)

ls = []

for i in range(4, argc):
    ls.append(int(sys.argv[i]))

board = np.array(ls).reshape(size_y, size_x)
copy = np.array(board, copy = True)
found = False

def minetest(bd, x, y):
    limit = bd[y][x]
    cnt = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if (i < 0 or i >= size_x):
                continue
            if (j < 0 or j >= size_y):
                continue
            if (bd[j][i] == -2):
                cnt += 1
            if (cnt > limit):
                break
    if (cnt != limit):
        return False
    else:
        return True

def countmine(bd):
    count = 0
    for i in range(size_x):
        for j in range(size_y):
            if (bd[j][i] == -2):
                count += 1

    return count


def check(bd):
    for j in range(size_y):
        for i in range(size_x):
            if (bd[j][i] >= 0):
                ret = minetest(bd, i, j)
                if (ret == False):
                    return False
    return True


def backtrack(bd, x, y):
    global found
    if found:
        return True
    if (x >= size_x or y >= size_y):
        ret = check(bd)
        if (ret == True and countmine(bd) == mines):
            global ans
            ans = np.array(bd, copy = True)
            found = True
        return

    child = np.array(bd, copy = True)
    if (board[y][x] == -1 and countmine(bd) < mines):
        child[y][x] = -2
        print(child)
    new_x = (x + 1) % size_x
    new_y = y
    if (new_x == 0):
        new_y += 1

    if (new_y < size_y and new_x < size_x):
        while (board[new_y][new_x] != -1):
            new_x = (new_x + 1) % size_x
            new_y = new_y
            if (new_x == 0):
                new_y += 1
            if (new_y >= size_y or new_x >= size_x):
                break
    backtrack(child, new_x, new_y)
    if (board[y][x] == -1):
        child[y][x] = -5
        print(child)
    backtrack(child, new_x, new_y)

def printboard():
    for j in range(size_y):
        for i in range(size_x):
            if (ans[j][i] == -2):
                print(" * ", end = "")
            elif (ans[j][i] == -5 or ans[j][i] == -1):
                print(" ~ ", end = "")
            else:
                print(" %d "%ans[j][i], end = "")
        print("")

time1 = time.time()
backtrack(copy, 0, 0)
time2 = time.time()
elapse = time2 - time1

try:
    printboard()
    print("elapsed time: %ss"%str(elapse))
except:
    print("no solution")

##
## test = np.array([-1,-2,-1,1,1,-1,
##                  -2,3,-1,-2,-1,0,
##                  2,3,-2,3,3,2,
##                  -1,-2,2,-1,-2,-2,
##                  -1,2,2,3,-1,3,
##                  -2,1,-1,-2,-2,1]).reshape(6,6)
## print(check(test))
