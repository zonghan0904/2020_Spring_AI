class DecisionTree():
    def __init__(self, file_name):
        self.file_name = file_name
        self.data_x = []
        self.data_y = []

    def load_data(self):
        with open(self.file_name, "r") as f:
            l = f.readline()
            counter = 0
            while (l):
                self.data_x.append(l.split(",")[:4])
                self.data_y.append(l.split(",")[4].strip("\n"))
                l = f.readline()
                counter += 1
        # print(self.data_x)
        # print(self.data_y)


if __name__ == "__main__":
    tree = DecisionTree("iris.data")
    tree.load_data()
