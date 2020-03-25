from argparse import ArgumentParser

description = """This is Introduction to AI course homework 1.
you can input the type of algorithm list below :
    0  ---  BFS
    1  ---  DFS
    2  ---  IDS
    3  ---  A*
    4  ---  IDA*\n"""
print(description)

parser = ArgumentParser()
parser.add_argument("algo_num", type=int, help="choose a algorithm.")
parser.add_argument("sx", type=int, help="assign starting x.")
parser.add_argument("sy", type=int, help="assign starting x.")
parser.add_argument("gx", type=int, help="assign goal x.")
parser.add_argument("gy", type=int, help="assign goal y.")

args = parser.parse_args()

class ChessBoard():
    def __init__(self, args):
        self.algo = args.algo_num
        self.sx = args.sx
        self.sy = args.sy
        self.gx = args.gx
        self.gy = args.gy
        self.explored = set()
        self.frontier = []

    def BFS():
        pass

    def DFS():
        pass

    def IDS():
        pass

    def A_star():
        pass

    def IDA_star():
        pass

if __name__ == "__main__":
    chessboard = ChessBoard(args)
    # print(chessboard.explored)
