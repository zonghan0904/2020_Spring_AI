from argparse import ArgumentParser

description = """This is Introduction to AI course homework 1.
you should input the type of algorithm list below :
    0  ---  BFS
    1  ---  DFS
    2  ---  IDS
    3  ---  A*
    4  ---  IDA*\n"""
print(description)

parser = ArgumentParser()
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
        self.cur_x = self.sx
        self.cur_y = self.sy
        self.gx = args.gx
        self.gy = args.gy
        self.explored = set()
        self.frontier = [(args.sx, args.sy)]
        self.path = dict()

    def BFS(self):
        while 1:
            if len(self.frontier) == 0:
                print("sorry, no route can acheive goal point.")
                break
            elif self.is_goal():
                print("arrived goal point, the shortest path is :")
                self.PrintPath()
                break
            else:
                self.BFS_expand()

    def DFS(self):
        pass

    def IDS(self):
        pass

    def A_star(self):
        pass

    def IDA_star(self):
        pass

    def BFS_expand(self):
        self.cur_x, self.cur_y = self.frontier[0][0], self.frontier[0][1]
        self.explored.add(self.frontier[0])
        del self.frontier[0]

        if self.allow((self.cur_x + 1, self.cur_y + 2)):
            self.frontier.append((self.cur_x + 1, self.cur_y + 2))
            self.path[(self.cur_x + 1, self.cur_y + 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x + 1, self.cur_y - 2)):
            self.frontier.append((self.cur_x + 1, self.cur_y - 2))
            self.path[(self.cur_x + 1, self.cur_y - 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 1, self.cur_y + 2)):
            self.frontier.append((self.cur_x - 1, self.cur_y + 2))
            self.path[(self.cur_x - 1, self.cur_y + 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 1, self.cur_y - 2)):
            self.frontier.append((self.cur_x - 1, self.cur_y - 2))
            self.path[(self.cur_x - 1, self.cur_y - 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x + 2, self.cur_y + 1)):
            self.frontier.append((self.cur_x + 2, self.cur_y + 1))
            self.path[(self.cur_x + 2, self.cur_y + 1)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x + 2, self.cur_y - 1)):
            self.frontier.append((self.cur_x + 2, self.cur_y - 1))
            self.path[(self.cur_x + 2, self.cur_y - 1)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 2, self.cur_y + 1)):
            self.frontier.append((self.cur_x - 2, self.cur_y + 1))
            self.path[(self.cur_x - 2, self.cur_y + 1)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 2, self.cur_y - 1)):
            self.frontier.append((self.cur_x - 2, self.cur_y - 1))
            self.path[(self.cur_x - 2, self.cur_y - 1)] = (self.cur_x, self.cur_y)

    def DFS_expand(self):
        self.cur_x, self.cur_y = self.frontier[0][0], self.frontier[0][1]

        if self.allow((self.cur_x + 1, self.cur_y + 2)):
            self.frontier.append((self.cur_x + 1, self.cur_y + 2))
            self.path[(self.cur_x + 1, self.cur_y + 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x + 1, self.cur_y - 2)):
            self.frontier.append((self.cur_x + 1, self.cur_y - 2))
            self.path[(self.cur_x + 1, self.cur_y - 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 1, self.cur_y + 2)):
            self.frontier.append((self.cur_x - 1, self.cur_y + 2))
            self.path[(self.cur_x - 1, self.cur_y + 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 1, self.cur_y - 2)):
            self.frontier.append((self.cur_x - 1, self.cur_y - 2))
            self.path[(self.cur_x - 1, self.cur_y - 2)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x + 2, self.cur_y + 1)):
            self.frontier.append((self.cur_x + 2, self.cur_y + 1))
            self.path[(self.cur_x + 2, self.cur_y + 1)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x + 2, self.cur_y - 1)):
            self.frontier.append((self.cur_x + 2, self.cur_y - 1))
            self.path[(self.cur_x + 2, self.cur_y - 1)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 2, self.cur_y + 1)):
            self.frontier.append((self.cur_x - 2, self.cur_y + 1))
            self.path[(self.cur_x - 2, self.cur_y + 1)] = (self.cur_x, self.cur_y)
        if self.allow((self.cur_x - 2, self.cur_y - 1)):
            self.frontier.append((self.cur_x - 2, self.cur_y - 1))
            self.path[(self.cur_x - 2, self.cur_y - 1)] = (self.cur_x, self.cur_y)

        self.explored.add(self.frontier[0])
        del self.frontier[0]

    def allow(self, pos):
        x, y = pos[0], pos[1]
        if x > 7 or x < 0:
            return False
        elif y > 7 or y < 0:
            return False
        elif (x, y) in self.explored:
            return False
        else:
            return True

    def is_goal(self):
        if (self.cur_x, self.cur_y) == (self.gx, self.gy):
            return True
        else:
            return False

    def PrintPath(self):
        path = []
        pos = (self.gx, self.gy)
        path.insert(0, pos)

        while pos != (self.sx, self.sy):
            pos = self.path[pos]
            path.insert(0, pos)

        for i in path:
            print(i, end=" ")

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
    # print(chessboard.explored)
