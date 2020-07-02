import numpy as np
import random
import math
import collections
# np.random.seed(0)

######## HYPER PARAMETERS ########
ATTR_NUM = 34
VALID_RATIO = 0.2
SAMPLING_RATE = 0.3
TREE_NUM = 1
FILE_NAME = "ionosphere.data"
TEST_CNT = 10
##################################

class Node():
    """
    the node in decision tree.
    discribe spliting attribute and threshold.
    """
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
    """
    decision tree using CART as base tree.
    """
    def __init__(self, data_x = None, data_y = None):
        self.root = Node(None, None)
        self.attr_num = ATTR_NUM
        self.bagging = int(math.sqrt(self.attr_num))

        if (data_x != None and data_y != None):
            self.root.data_x = data_x
            self.root.data_y = data_y

    def load_data(self, file_name):
        """
        load dataset downloaded from UCI Machine Learning Repository.
        """
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
        """
        return how many classes in current node.
        """
        num = len(set(node.data_y))
        return num

    def attr_selector(self, node, attr_ls = []):
        """
        according to gini's inpurity to select an attribute and threshold.
        """
        best_attr = -1
        best_thre = 0.0
        lowest_impurity = float("inf")
        attrs = []
        if attr_ls == []:
            attrs = list(np.arange(self.attr_num))
        else:
            attrs = list(attr_ls)
        n = len(node.data_x)

        for attr in attrs:
            values = set()
            for data in node.data_x:
                values.add(data[attr])
            values = list(values)
            values.sort()

            length = len(values)
            for j in range(length-1):
                thre = (values[j] + values[j+1]) / 2
                right = {key: 0 for key in node.data_y}
                left = {key: 0 for key in node.data_y}

                for k in range(n):
                    if (node.data_x[k][attr] > thre):
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
                    best_attr = attr

        return best_attr, best_thre


    def build_tree(self, node):
        """
        the core of decision tree's training part.
        function will keep recursively calling itselt until reach leaf nodes.
        """
        num = self.num_classes(node)

        if num == 1:
            node.leaf = True
            node.label = node.data_y[0]
        else:
            attr_ls = random.sample(list(np.arange(self.attr_num)), k = self.bagging)
            attr, thre = self.attr_selector(node, attr_ls)
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
        """
        train decision tree.
        """
        self.build_tree(self.root)

    def path(self, node, data):
        """
        to find the predicted answer.
        """
        if (node.leaf == True):
            self.predicted_ans = node.label
        else:
            if (data[node.attr] < node.thre):
                self.path(node.left, data)
            else:
                self.path(node.right, data)

    def predict(self, data):
        """
        get the predicted answer.
        """
        self.path(self.root, data)
        return self.predicted_ans

class RandomForest():
    """
    random forest features tree bagging and attribute bagging.
    """
    def __init__(self):
        self.data_x = []
        self.data_y = []
        self.data_cnt = 0
        self.trees = []
        self.valid_ratio = VALID_RATIO
        self.sampling_rate = SAMPLING_RATE
        self.attr_num = ATTR_NUM

    def load_data(self, file_name):
        """
        load dataset downloaded from UCI Machine Learning Repository.
        """
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
        """
        splitting data into training subset and validation subset.
        """
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
        """
        randomly sampling small part of data.
        """
        sample_cnt = int(self.sampling_rate * self.train_cnt)
        data_ls = np.random.permutation(np.arange(self.train_cnt))[:sample_cnt]
        data_x = []
        data_y = []

        for i in data_ls:
            data_x.append(self.train_x[i])
            data_y.append(self.train_y[i])

        return data_x, data_y

    def gen_forest(self, tree_num = 3):
        """
        generate decision trees to build the random forest.
        """
        print("\n[INFO] Start generating random forest ...")
        self.tree_num = tree_num
        for i in range(self.tree_num):
            data_x, data_y = self.tree_bagging()
            t = DecisionTree(data_x, data_y)
            self.trees.append(t)
            print("finish %d / %d" %(i+1, self.tree_num))

    def train(self):
        """
        train each decision trees in the random forest.
        """
        print("\n[INFO] Start training ...")
        i = 0
        for tree in self.trees:
            tree.train()
            print("finish %d / %d" %(i+1, self.tree_num))
            i += 1

    def predict(self, data):
        """
        get the predicted answer via voting among decision trees.
        """
        answers = []
        for tree in self.trees:
            predicted_ans = tree.predict(data)
            answers.append(predicted_ans)
        ans = collections.Counter(answers).most_common()[0][0]
        return ans

    def validation(self):
        """
        using validation subset to test the model.
        will return the predicted accuracy.
        """
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
        # print("correct num: %d" %correct_num)
        acc = correct_num / self.valid_cnt
        print("correct classification rates: {a}%".format(a = acc * 100))
        return acc

    def get_info(self):
        """
        return the model's information.
        """
        info = "######### FOREST INFO #########\n" + \
               "file: %s\n"%FILE_NAME + \
               "tree number: %d\n"%self.tree_num + \
               "valid ratio: %f\n"%self.valid_ratio + \
               "sampling rate: %f\n"%self.sampling_rate + \
               "attribute number: %d\n"%self.attr_num + \
               "###############################\n\n"
        return info

    def save_result(self, acc):
        """
        saving the validation result.
        """
        info = self.get_info()
        result = info + "correct classification rates: {a}%\n\n".format(a = acc * 100)
        file_name = "experiment/tree-num-%d.txt"%self.tree_num
        with open(file_name, "a") as f:
            f.write(result)
        print("\n[INFO] Result saved to %s ..."%file_name)


if __name__ == "__main__":
    # tree = DecisionTree()
    # tree.load_data("iris.data")
    # tree.train()
    # tree.predict([5.0,3.4,1.5,0.2])

    ############################## test case ##############################
    ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    #######################################################################

    for num in nums:
        TREE_NUM = num
        for ratio in ratios:
            VALID_RATIO = ratio
            acc = 0
            for i in range(TEST_CNT):                   # experiment multiple times to average out the noises.
                forest = RandomForest()
                forest.load_data(FILE_NAME)
                forest.data_split()
                forest.gen_forest(tree_num = TREE_NUM)
                forest.train()
                acc += forest.validation()
            forest.save_result(acc / TEST_CNT)

    # ans = forest.predict([6.3,2.5,5.0,1.9])
    # print(ans)
