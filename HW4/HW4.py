import numpy as np
import collections
# np.random.seed(0)

######## HYPER PARAMETERS ########
ATTR_NUM = 4
VALID_RATIO = 0.2
SAMPLING_RATE = 0.6
TREE_NUM = 5
##################################

class Node():
    def __init__(self, attr, thre):
        self.attr = attr
        self.thre = thre
        self.left = None
        self.right = None
        self.leaf = False
        self.data_x = []
        self.data_y = []
        self.label = ""

class DecisionTree():
    def __init__(self, data_x = None, data_y = None):
        self.root = Node(None, None)
        self.attr_num = ATTR_NUM

        if (data_x != None and data_y != None):
            self.root.data_x = data_x
            self.root.data_y = data_y

    def load_data(self, file_name):
        with open(file_name, "r") as f:
            l = f.readline()
            while (l):
                self.root.data_x.append(l.split(",")[:self.attr_num])
                self.root.data_y.append(l.split(",")[self.attr_num].strip("\n"))
                l = f.readline()
        for i in range(len(self.root.data_x)):
            for j in range(self.attr_num):
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
            node.label = node.data_y[0]
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

    def path(self, node, data):
        if (node.leaf == True):
            self.predicted_ans = node.label
        else:
            if (data[node.attr] < node.thre):
                self.path(node.left, data)
            else:
                self.path(node.right, data)

    def predict(self, data):
        self.path(self.root, data)
        return self.predicted_ans

class RandomForest():
    def __init__(self):
        self.data_x = []
        self.data_y = []
        self.data_cnt = 0
        self.trees = []
        self.valid_ratio = VALID_RATIO
        self.sampling_rate = SAMPLING_RATE
        self.attr_num = ATTR_NUM

    def load_data(self, file_name):
        with open(file_name, "r") as f:
            l = f.readline()
            counter = 0
            while (l):
                self.data_x.append(l.split(",")[:self.attr_num])
                self.data_y.append(l.split(",")[self.attr_num].strip("\n"))
                l = f.readline()
                counter += 1
            self.data_cnt = counter

        for i in range(len(self.data_x)):
            for j in range(self.attr_num):
                self.data_x[i][j] = float(self.data_x[i][j])

        self.valid_cnt = int(self.valid_ratio * self.data_cnt)
        self.train_cnt = self.data_cnt - self.valid_cnt

    def data_split(self):
        train_ls = np.random.permutation(np.arange(self.data_cnt))[:self.train_cnt]
        valid_ls = []
        for i in range(self.data_cnt):
            if i not in set(train_ls):
                valid_ls.append(i)
        self.train_x = []
        self.train_y = []
        self.valid_x = []
        self.valid_y = []
        for i in train_ls:
            self.train_x.append(self.data_x[i])
            self.train_y.append(self.data_y[i])
        for i in valid_ls:
            self.valid_x.append(self.data_x[i])
            self.valid_y.append(self.data_y[i])

    def tree_bagging(self):
        sample_cnt = int(self.sampling_rate * self.train_cnt)
        data_ls = np.random.permutation(np.arange(self.train_cnt))[:sample_cnt]
        data_x = []
        data_y = []

        for i in data_ls:
            data_x.append(self.train_x[i])
            data_y.append(self.train_y[i])

        return data_x, data_y

    def gen_forest(self, tree_num = 3):
        print("\n[INFO] Start generating random forest ...")
        self.tree_num = tree_num
        for i in range(self.tree_num):
            data_x, data_y = self.tree_bagging()
            t = DecisionTree(data_x, data_y)
            self.trees.append(t)
            print("finish %d / %d" %(i+1, self.tree_num))

    def train(self):
        print("\n[INFO] Start training ...")
        i = 0
        for tree in self.trees:
            tree.train()
            print("finish %d / %d" %(i+1, self.tree_num))
            i += 1

    def predict(self, data):
        answers = []
        for tree in self.trees:
            predicted_ans = tree.predict(data)
            answers.append(predicted_ans)
        ans = collections.Counter(answers).most_common()[0][0]
        return ans

    def validation(self):
        print("\n[INFO] Start validation ...")
        acc = 0.0
        correct_num = 0
        for i in range(self.valid_cnt):
            ans = self.predict(self.valid_x[i])
            if ans == self.valid_y[i]:
                correct_num += 1
            # else:
            #     print("predicted: %s, answer: %s"%(ans, self.valid_y[i]))
            print("finish %d / %d" %(i+1, self.valid_cnt))
        print("correct num: %d" %correct_num)
        acc = correct_num / self.valid_cnt
        print("correct classification rates: {a}%".format(a = acc * 100))

if __name__ == "__main__":
    # tree = DecisionTree()
    # tree.load_data("iris.data")
    # tree.train()
    # tree.predict([5.0,3.4,1.5,0.2])

    forest = RandomForest()
    forest.load_data("iris.data")
    forest.data_split()
    forest.gen_forest(tree_num = TREE_NUM)
    forest.train()
    # ans = forest.predict([6.3,2.5,5.0,1.9])
    # print(ans)
    forest.validation()
