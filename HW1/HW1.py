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
        self.frontier = [(args.sx, args.sy)]
        self.path = dict()
        self.find = False
        self.algo_dict = {0: "BFS", 1: "DFS", 2: "IDS", 3:"A*", 4:"IDA*"}
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
        pass

    def IDA_star(self):
        pass

    def expand(self, counter):
        if counter <= 0:
            return False
        x, y = self.frontier[0][0], self.frontier[0][1]
        self.explored.add(self.frontier[0])
        del self.frontier[0]

        self.GoalTest((x, y))

        if (not self.find) and self.allow((x + 1, y + 2)):
            self.frontier.append((x + 1, y + 2))
            self.path[(x + 1, y + 2)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)
        if (not self.find) and self.allow((x + 1, y - 2)):
            self.frontier.append((x + 1, y - 2))
            self.path[(x + 1, y - 2)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)
        if (not self.find) and self.allow((x - 1, y + 2)):
            self.frontier.append((x - 1, y + 2))
            self.path[(x - 1, y + 2)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)
        if (not self.find) and self.allow((x - 1, y - 2)):
            self.frontier.append((x - 1, y - 2))
            self.path[(x - 1, y - 2)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)
        if (not self.find) and self.allow((x + 2, y + 1)):
            self.frontier.append((x + 2, y + 1))
            self.path[(x + 2, y + 1)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)
        if (not self.find) and self.allow((x + 2, y - 1)):
            self.frontier.append((x + 2, y - 1))
            self.path[(x + 2, y - 1)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)
        if (not self.find) and self.allow((x - 2, y + 1)):
            self.frontier.append((x - 2, y + 1))
            self.path[(x - 2, y + 1)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)
        if (not self.find) and self.allow((x - 2, y - 1)):
            self.frontier.append((x - 2, y - 1))
            self.path[(x - 2, y - 1)] = (x, y)
            if self.algo == 1:
                self.expand(counter)
            if self.algo == 2:
                self.expand(counter - 1)

    def allow(self, pos):
        x, y = pos[0], pos[1]
        if x > 7 or x < 0:
            return False
        elif y > 7 or y < 0:
            return False
        elif (x, y) in self.explored:
            return False
        elif (x, y) in self.frontier:
            return False
        else:
            return True

    def is_goal(self, pos):
        if pos == (self.gx, self.gy):
            return True
        else:
            return False

    def GoalTest(self, pos):
        self.find = self.is_goal((pos[0] + 1, pos[1] + 2))
        self.find = self.is_goal((pos[0] + 1, pos[1] - 2))
        self.find = self.is_goal((pos[0] - 1, pos[1] + 2))
        self.find = self.is_goal((pos[0] - 1, pos[1] - 2))
        self.find = self.is_goal((pos[0] + 2, pos[1] + 1))
        self.find = self.is_goal((pos[0] + 2, pos[1] - 1))
        self.find = self.is_goal((pos[0] - 2, pos[1] + 1))
        self.find = self.is_goal((pos[0] - 2, pos[1] - 1))

        if self.find:
            self.path[(self.gx, self.gy)] = (pos[0], pos[1])

    def PrintPath(self):
        path = []
        pos = (self.gx, self.gy)
        path.insert(0, pos)

        while pos != (self.sx, self.sy):
            pos = self.path[pos]
            path.insert(0, pos)

        for i in path:
            print(i, end=" ")

    def initialize(self):
        while len(self.frontier) != 0:
            self.frontier.pop()
        self.frontier.append((self.sx, self.sy))
        self.explored.clear()
        self.path.clear()

if __name__ == "__main__":
    chessboard = ChessBoard(args)
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

    print("\n###############################  INFO  ###############################\n")
    info = "using algorithm: %s\n"%(chessboard.algo_dict[chessboard.algo]) +\
    "start point: (%d, %d)\n"%(chessboard.sx, chessboard.sy) +\
    "goal  point: (%d, %d)\n"%(chessboard.gx, chessboard.gy)
    print(info)

    print("\n############################### RESULT ###############################\n")
    if chessboard.find:
        print("the shortest path is :\n")
        chessboard.PrintPath()
    else:
        print("with [%s] algorithm, the shortest path is :"%chessboard.algo_dict[chessboard.algo])
        print("sorry, no route can acheive goal point.")
