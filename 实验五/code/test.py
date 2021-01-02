import numpy as np

B = "1,2,3,4,5,56,2"
B = list(map(int,B.split(",")[3:]))
B.append(1)
print(B)

A = np.array([[2,1,3,4],[2,3,1,4],[3,2,2,1]])
A[:,1] = (A[:,1] - min(A[:,1])) / (max(A[:,1]) - min(A[:,1]))
print(A)
print(np.square(A).sum())
x = A.tolist()
print(x)

C = np.zeros(10)
print(C)