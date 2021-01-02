import numpy as np

class KDNode(object):
    def __init__(self, dimension, seperation):
        self.dimension = dimension
        self.seperation = seperation
        self.left = None
        self.right = None
        self.dots = []


def read_data():
    with open("kdd.txt", 'r') as f:
        data = f.read()
    data = data.split("\n")
    data = list(map(lambda x: x.split(",")[4:], data))
    flag_list = list(map(lambda x: 0 if x[-1] == 'normal' else 1, data))
    data = list(map(lambda x: x[:-1], data))
    data = list(map(lambda x: list(map(float, x)), data))
    # print(flag_list)
    for i in range(len(data)):
        data[i].append(flag_list[i])
    return data

def pre_treat(row_data):
    data = np.array(row_data)
    (data_count, dimension_count) = data.shape
    for i in range(dimension_count - 1):
        if max(data[:,i]) != min(data[:,i]):
            data[:,i] = (data[:,i]-min(data[:,i]))/(max(data[:,i])-min(data[:,i]))
    print(data)
    return data

def create_node(data):
    (data_count, dimension_count) = data.shape
    variance = np.zeros(dimension_count - 1)
    for i in range(dimension_count - 1):
        variance[i] = np.square((data[:,i] - data[:, i].mean())).sum()
    dimension = np.where(variance == max(variance))
    print(data_count)
    # dimension_count = len(data[0])
    # data_count = len(data)
    # width_list = []
    # for i in range(dimension_count):
    #     width_list.append(max(data[:, i]) - min(data[:, i]))
    # dimension = width_list.index(max(width_list))
    seperation = np.mean(np.sort(data[:, dimension[0]])[data_count // 2 - 1 : data_count // 2 + 1])
    
    return KDNode(dimension[0], seperation)

if __name__ == "__main__":
    row_data = read_data()
    data = pre_treat(row_data)
    # print(data)

    node = create_node(data)
    d = node.dimension
    s = node.seperation
    print(d)
    print("............")
    print(s)
