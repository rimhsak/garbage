import numpy as np

#np.append([1,2,3], [3,4,5], [6,7,8])
a1 = np.asarray([1, 2, 3, 4])
a2 = np.asarray([3, 4, 5, 5])
a3 = np.asarray([6, 7, 8, 9])
c = np.array([5,6])

a= np.vstack([a1, a2])
print(a)
print(a.shape)
print(a3.shape)
print(c.shape)
b = np.vstack([a, a3])
print(b)
print(b.shape)

A = np.zeros([3,4])
print(A)
A[0] = a1
A[1] = a2
A[2] = a3
print(A)