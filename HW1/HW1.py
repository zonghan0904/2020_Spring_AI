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
        self.algo = args.algo_num
        self.cur_x = args.sx
        self.cur_y = args.sy
        self.gx = args.gx
        self.gy = args.gy
        self.explored = set()
        self.frontier = [(args.sx, args.sy)]
        self.path = dict()

    def BFS(self):
        pass

    def DFS(self):
        pass

    def IDS(self):
        pass

    def A_star(self):
        pass

    def IDA_star(self):
        pass

    def expand(self):
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
        pos[0], pos[1] = x, y
        if x > 7 or x < 0:
            return False
        elif y > 7 or y < 0:
            return False
        elif (x, y) in self.explored:
            return False
        else:
            return True

if __name__ == "__main__":
    chessboard = ChessBoard(args)
    # print(chessboard.explored)
