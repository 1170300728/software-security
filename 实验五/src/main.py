import numpy as np


def process(path):

    f = open(path, "r", encoding="utf8")
    f_train = open("train.csv", "w", encoding="utf8")
    f_test = open("test.csv", "w", encoding="utf8")
    line = f.readline()
    for i in range(10000):
        line = f.readline()
    train_line_number = 0
    test_normal_line_number = 0
    test_smurf_line_number = 0
    while line:
        split_line = line.split(",")
        label = split_line[41].rstrip(".\n")
        line_write = ""
        for word in split_line[20:30]:
            line_write += word + ","
        line_write.rstrip(",")
        if label == "normal":
            if train_line_number < 60000:
                train_line_number += 1
                f_train.write(line_write + "\n")
            else:
                if test_normal_line_number < 500:
                    test_normal_line_number += 1
                    f_test.write(line_write + label + "\n")
        elif label == "smurf":
            if test_smurf_line_number < 500:
                test_smurf_line_number += 1
                f_test.write(line_write + label + "\n")
        line = f.readline()
    f.close()
    f_test.close()
    f_train.close()


def read_data(path):
    with open(path, "r", encoding="utf8") as f:
        data = []
        line = f.readline()
        while line:
            data.append([float(x) for x in line.rstrip(",\n").split(",")])
            line = f.readline()
        return data


def read_test(path):
    with open(path, "r", encoding="utf8") as f:
        data = []
        line = f.readline()
        while line:
            split_line = line.rstrip(",\n").split(",")
            label = split_line[-1]
            data_line = [float(x) for x in split_line[:-1]]
            if label == "normal":
                data.append([data_line, 1])
            else:
                data.append([data_line, 0])
            line = f.readline()
        return data


class KDNode(object):
    def __init__(self, value=None, label=None, dim=None, parent=None, left_child=None, right_child=None):
        """
        初始化KDNode的属性
        :param value: 节点的值
        :param label: 标签：0表示smurf，1代表normal
        :param dim: 数据的维度
        :param parent: 父节点
        :param left_child: 左子节点
        :param right_child: 右子节点
        """
        self.value = value
        self.label = label
        self.dim = dim
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child


class KDTree:
    def __init__(self, data, dataLabel):
        self.__length = 0
        self.__root = self.__create(data, dataLabel)
        self.threhold = 5

    @property
    def length(self):
        return self.__length

    @property
    def root(self):
        return self.__root

    def __create(self, data, dataLabel, parentNode=None):
        numpyData = np.array(data)
        l, w = numpyData.shape
        if l == 0:
            return None
        numpyLabel = np.array(dataLabel).reshape(l, -1)

        varList = [np.var(numpyData[:, i]) for i in range(w)]
        maxVarIndex = varList.index(max(varList))
        maxFeature = numpyData[:, maxVarIndex].argsort()
        midValueIndex = maxFeature[l // 2]
        if l == 1:  # 当数据的长度为1时，不需要继续分离
            self.__length += 1
            return KDNode(dim=maxVarIndex, label=numpyLabel[midValueIndex], value=numpyData[midValueIndex],
                          parent=parentNode)
        kdNode = KDNode(dim=maxVarIndex, label=numpyLabel[midValueIndex], value=numpyData[midValueIndex],
                        parent=parentNode)
        return self.divideChildren(numpyData, numpyLabel, maxFeature, l, kdNode)

    def divideChildren(self, data, label, maxFeature, length, node):
        """
        构建左右子树到父节点上
        :param data: 总数据
        :param label: 总label
        :param maxFeature: 最大的方差列
        :param length: 数据的长度
        :param node: 父节点
        :return:
        """
        leftData = data[maxFeature[:length // 2]]
        rightData = data[maxFeature[length // 2 + 1:]]
        leftLabel = label[maxFeature[:length // 2]]
        rightLabel = label[maxFeature[length // 2 + 1:]]
        left_child = self.__create(leftData, leftLabel, node)
        if length == 2:
            right_child = None
        else:
            right_child = self.__create(rightData, rightLabel, node)
        node.left_child, node.right_child = left_child, right_child
        self.__length += 1
        return node

    def tree2List(self, tree_node, input_list=None):
        if input_list is None:
            input_list = []
        if tree_node is None:
            return None
        output_dict = {'value': tuple(tree_node.value), 'label': tree_node.label[0], 'dim': tree_node.dim,
                       'parent': tuple(tree_node.parent.item) if tree_node.parent else None,
                       'left_child': tuple(tree_node.left_child.item) if tree_node.left_child else None,
                       'right_child': tuple(tree_node.right_child.item) if tree_node.right_child else None}
        input_list.append(output_dict)
        self.tree2List(tree_node.left_child, input_list)
        self.tree2List(tree_node.right_child, input_list)
        return input_list

    def _getNearestNeighour(self, value):
        if self.length == 0:
            return None
        node = self.__root
        if self.length == 1:
            return node
        while True:
            currentDim = node.dim
            if value[currentDim] > node.value[currentDim]:
                if node.right_child is None:
                    return node
                node = node.right_child
            elif value[currentDim] < node.value[currentDim]:
                if node.left_child is None:
                    return node
                node = node.left_child
            else:
                return node
    def get_distance(self, nodeList, k):
        if k>=len(nodeList):
            least_distance = nodeList[-1][0]
        else:
            least_distance = nodeList[k - 1][0]
        return least_distance

    def middleOrder(self, value, node, nodeList, k):
        """
        中序遍历子树节点（左，根，右）
        :param value:
        :param node:
        :param nodeList:
        :param k:
        :return:
        """
        nodeList.sort()
        least_distance = self.get_distance(nodeList, k)
        if node.left_child is None and node.right_child is None:
            distance = np.sqrt(sum(value-node.value)**2)
            if k > len(nodeList) or distance < least_distance:
                nodeList.append([distance, tuple(node.value), node.label[0]])
            return
        self.middleOrder(value, node.left_child, nodeList, k)
        nodeList.sort()
        least_distance = self.get_distance(nodeList, k)
        distance = np.sqrt(sum(value-node.value)**2)
        if k > len(nodeList) or distance < least_distance:
            nodeList.append([distance, tuple(node.value), node.label[0]])
        if k > len(nodeList) or abs(value[node.dim] - node.value[node.dim]) < least_distance:
            if node.right_child is not None:
                self.middleOrder(value, node.right_child, nodeList, k)
        return nodeList

    def unMiddleOrder(self, value, node, nodeList, k):
        """
        逆中序遍历子树节点（右，根，左）
        :param value:
        :param node:
        :param nodeList:
        :param k:
        :return:
        """
        nodeList.sort()
        least_distance = self.get_distance(nodeList, k)
        if node.left_child is None and node.right_child is None:
            distance = np.sqrt(sum(value - node.value) ** 2)
            if k > len(nodeList) or distance < least_distance:
                nodeList.append([distance, tuple(node.value), node.label[0]])
            return
        if node.right_child is not None:
            self.unMiddleOrder(value, node.right_child, nodeList, k)
        nodeList.sort()
        least_distance = self.get_distance(nodeList, k)
        distance = np.sqrt(sum(value - node.value) ** 2)
        if k > len(nodeList) or distance < least_distance:
            nodeList.append([distance, tuple(node.value), node.label[0]])
        if k > len(nodeList) or abs(value[node.dim] - node.value[node.dim]) < least_distance:
            if node.right_child is not None:
                self.unMiddleOrder(value, node.left_child, nodeList, k)
        return nodeList

    def knn(self, input_list, k):
        input_array = np.array(input_list)
        tree_node = self._getNearestNeighour(input_array)
        if tree_node is None:
            return None
        nodes = []
        distance = np.sqrt(sum((input_array - tree_node.value) ** 2))
        min_distance = distance
        nodes.append([distance, tuple(tree_node.value), tree_node.label[0]])
        if tree_node.left_child is not None:
            left_child = tree_node.left_child
            left_distance = np.sqrt(sum(input_array - left_child.value) ** 2)
            if k > len(nodes):
                nodes.append([left_distance, tuple(left_child.value), left_child.label[0]])
                nodes.sort()
                if k >= len(nodes):
                    min_distance = nodes[-1][0]
                else:
                    min_distance = nodes[k-1][0]
        while True:
            if tree_node == self.root:
                break
            parent = tree_node.parent
            parent_distance = np.sqrt(sum((input_array - parent.value) ** 2))
            if k > len(nodes) or parent_distance < min_distance:
                nodes.append([parent_distance, tuple(parent.value), parent.label[0]])
                nodes.sort()
            if k > len(nodes) or abs(input_array[parent.dim] - parent.value[parent.dim]) < min_distance:
                if parent.left_child != tree_node:
                    the_other_child = parent.left_child
                else:
                    the_other_child = parent.right_child
                if the_other_child is not None:
                    if input_array[parent.dim] - parent.value[parent.dim] <= 0:
                        self.middleOrder(input_array, the_other_child, nodes, k)
                    else:
                        self.unMiddleOrder(input_array, the_other_child, nodes, k)
            tree_node = parent
        nodes = nodes[:k]
        if nodes[0][0] >= self.threhold:
            label = 0
        else:
            label = 1
        return label, nodes


if __name__ == '__main__':
    process("data.txt")
    train_data = read_data("train.csv")
    test_data = read_test("test.csv")
    tree = KDTree(train_data, np.random.randint(1, 2, size=(60000, 1)))
    hit_count = 0
    fp = 0
    fn = 0
    normal = 0
    smurf = 0
    for data in test_data:
        test_list = data[0]
        true_label = data[1]
        label, node_list = tree.knn(test_list, 1)
        if true_label == label:
            if label == 0:
                hit_count += 1
            else:
                normal += 1
        elif true_label == 1 and label == 0:
            fp += 1
        elif true_label == 0 and label == 1:
            fn += 1
    tpr = float(hit_count) / float(hit_count + fn)
    fpr = float(fp) / float(normal + fp)
    print("运行完成! ")
    print("-------------------")
    print("异常数|{}个".format(hit_count))
    print("召回率|{:.2f}%".format(tpr * 100))
    print("误报率|{:.2f}%".format(fpr * 100))
    print("漏报率|{:.2f}%".format((1 - tpr) * 100))
    print("-------------------")
