import time
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

description = """This is Introduction to AI course homework 1.
you should input the type of algorithm list below :
    0  ---  BFS
    1  ---  DFS
    2  ---  IDS
    3  ---  A*
    4  ---  IDA*"""

parser = ArgumentParser(description = description, formatter_class=RawTextHelpFormatter)
parser.add_argument("num", type=int, help="choose a algorithm.")
parser.add_argument("sx", type=int, help="assign starting x.")
parser.add_argument("sy", type=int, help="assign starting x.")
parser.add_argument("gx", type=int, help="assign goal x.")
parser.add_argument("gy", type=int, help="assign goal y.")

args = parser.parse_args()

class ChessBoard():
    def __init__(self, args):
        self.algo = args.num
        self.sx = args.sx
        self.sy = args.sy
        self.gx = args.gx
        self.gy = args.gy
        self.explored = set()
        self.frontier = [(args.sx, args.sy, 0)]
        self.path = dict()
        self.find = False
        self.algo_dict = {0: "BFS", 1: "DFS", 2: "IDS", 3:"A*", 4:"IDA*"}
        self.direction = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        self.iter_len = 1

    def BFS(self):
        while 1:
            if len(self.frontier) == 0:
                break
            elif self.find:
                break
            else:
                self.expand(1)

    def DFS(self):
        self.expand(1)

    def IDS(self):
        while (not self.find) and len(self.frontier) != 0:
            self.initialize()
            self.expand(self.iter_len)
            self.iter_len += 1

    def A_star(self):
        while 1:
            if len(self.frontier) == 0:
                break
            elif self.find:
                break
            else:
                self.expand(1)

    def IDA_star(self):
        while (not self.find) and len(self.frontier) != 0:
            self.initialize()
            self.expand(self.iter_len)
            self.iter_len += 1

    def expand(self, counter):
        if counter <= 0:
            return False
        if self.algo == 3 or self.algo == 4:
            self.frontier.sort(key=self.heuristic)

        x, y, cost = self.frontier[0][0], self.frontier[0][1], self.frontier[0][2]
        self.explored.add((self.frontier[0][0], self.frontier[0][1]))
        del self.frontier[0]

        self.GoalTest((x, y))
        if self.find:
            return True

        for direct in self.direction:
            if (not self.find) and self.allow((x + direct[0], y + direct[1])):
                if self.algo == 0 or self.algo == 3 or self.algo == 4:
                    self.frontier.append((x + direct[0], y + direct[1], cost + 1))
                elif self.algo == 1 or self.algo == 2:
                    self.frontier.insert(0, (x + direct[0], y + direct[1], cost + 1))

                self.path[(x + direct[0], y + direct[1])] = (x, y)

                if self.algo == 1:
                    self.expand(counter)
                if self.algo == 2 or self.algo == 4:
                    self.expand(counter - 1)

    def allow(self, pos):
        x, y = pos[0], pos[1]
        for i in self.frontier:
            if (x, y) == i[:2]:
                return False
        if x > 7 or x < 0:
            return False
        elif y > 7 or y < 0:
            return False
        elif (x, y) in self.explored:
            return False
        else:
            return True

    def is_goal(self, pos):
        if pos == (self.gx, self.gy):
            return True
        else:
            return False

    def GoalTest(self, pos):
        for direct in self.direction:
            self.find = self.is_goal((pos[0] + direct[0], pos[1] + direct[1]))
            if self.find:
                self.path[(self.gx, self.gy)] = (pos[0], pos[1])
                return True

    def PrintPath(self):
        path = []
        pos = (self.gx, self.gy)
        path.insert(0, pos)

        while pos != (self.sx, self.sy):
            pos = self.path[pos]
            path.insert(0, pos)

        for i in path:
            print(i, end=" ")

        steps = len(path) - 1
        print("\n\ntotal steps: %d\n"%steps)

    def initialize(self):
        while len(self.frontier) != 0:
            self.frontier.pop()
        self.frontier.append((self.sx, self.sy, 0))
        self.explored.clear()
        self.path.clear()

    def heuristic(self, pos):
        dx = abs(self.gx - pos[0])
        dy = abs(self.gy - pos[1])
        return (dx + dy) // 3 + pos[2]

if __name__ == "__main__":
    chessboard = ChessBoard(args)

    tick1 = time.clock()
    if args.num == 0:
        chessboard.BFS()
    elif args.num == 1:
        chessboard.DFS()
    elif args.num == 2:
        chessboard.IDS()
    elif args.num == 3:
        chessboard.A_star()
    elif args.num == 4:
        chessboard.IDA_star()
    else:
        print("algorithm type out of bound. please using [python HW1.py --help] to get more information.")
        print("setting default algorithm type [BFS].")
        chessboard.algo = 0
        chessboard.BFS()
    tick2 = time.clock()
    elapsed = tick2 - tick1

    print("\n###############################  INFO  ###############################\n")
    info = "using algorithm: %s\n"%(chessboard.algo_dict[chessboard.algo]) +\
    "start point: (%d, %d)\n"%(chessboard.sx, chessboard.sy) +\
    "goal  point: (%d, %d)\n"%(chessboard.gx, chessboard.gy)
    print(info)

    print("\n############################### RESULT ###############################\n")
    if chessboard.find:
        print("the shortest path is :\n")
        chessboard.PrintPath()
        print("elapsed time: %s"%elapsed)
    else:
        print("with [%s] algorithm, the shortest path is :"%chessboard.algo_dict[chessboard.algo])
        print("sorry, no route can acheive goal point.")

