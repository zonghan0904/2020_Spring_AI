class Node():
    def __init__(self, attr, thre):
        self.attr = attr
        self.thre = thre
        self.left = None
        self.right = None
        self.leaf = False
        self.data_x = []
        self.data_y = []

class DecisionTree():
    def __init__(self, file_name):
        self.file_name = file_name
        self.root = Node(None, None)
        self.attr_num = 4

    def load_data(self):
        with open(self.file_name, "r") as f:
            l = f.readline()
            counter = 0
            while (l):
                self.root.data_x.append(l.split(",")[:4])
                self.root.data_y.append(l.split(",")[4].strip("\n"))
                l = f.readline()
                counter += 1
        for i in range(len(self.root.data_x)):
            for j in range(4):
                self.root.data_x[i][j] = float(self.root.data_x[i][j])

    def num_classes(self, node):
        num = len(set(node.data_y))
        return num

    def attr_selector(self, node):
        best_attr = -1
        best_thre = 0.0
        lowest_impurity = float("inf")
        n = len(node.data_x)

        for i in range(self.attr_num):
            values = set()
            for data in node.data_x:
                values.add(data[i])
            values = list(values)
            values.sort()

            length = len(values)
            for j in range(length-1):
                thre = (values[j] + values[j+1]) / 2
                right = {key: 0 for key in node.data_y}
                left = {key: 0 for key in node.data_y}

                for k in range(n):
                    if (node.data_x[k][i] > thre):
                        right[node.data_y[k]] += 1
                    else:
                        left[node.data_y[k]] += 1

                nA = list(left.values())
                nB = list(right.values())
                GA = 0.0
                GB = 0.0

                sum_pk = 0.0
                for pk in nA:
                    sum_pk += (pk / sum(nA))**2
                GA = 1 - sum_pk

                sum_pk = 0.0
                for pk in nB:
                    sum_pk += (pk / sum(nB))**2
                GB = 1 - sum_pk

                remain = sum(nA) * GA + sum(nB) * GB
                if remain < lowest_impurity:
                    best_thre = thre
                    best_attr = i

        return best_attr, best_thre


    def build_tree(self, node):
        num = self.num_classes(node)

        if num == 1:
            node.leaf = True
        else:
            attr, thre = self.attr_selector(node)
            node.attr = attr
            node.thre = thre

            right = Node(None, None)
            left = Node(None, None)

            n = len(node.data_x)
            for i in range(n):
                if (node.data_x[i][attr] > thre):
                    right.data_x.append(node.data_x[i])
                    right.data_y.append(node.data_y[i])
                else:
                    left.data_x.append(node.data_x[i])
                    left.data_y.append(node.data_y[i])

            self.build_tree(right)
            self.build_tree(left)
            node.right = right
            node.left = left

    def train(self):
        self.build_tree(self.root)

    def predict(self, node, data):
        if (node.leaf == True):
            print(node.data_y[0])
        else:
            if (data[node.attr] < node.thre):
                self.predict(node.left, data)
            else:
                self.predict(node.right, data)


if __name__ == "__main__":
    tree = DecisionTree("iris.data")
    tree.load_data()
    tree.train()
    tree.predict(tree.root, [5.0,3.4,1.5,0.2])
