import numpy as np
from numpy import linalg as al

EPS = 0.00001
MAX_ITER = 10000

def differenceNorm(matr, vec, val):
	return al.norm(np.dot(matr, vec) - vec*val)

def frobeniusNorm(matr):
	tmp = 0
	for i in range(len(matr)):
		for j in range(len(matr)):
			tmp += pow(matr[i][j], 2)
	return pow(tmp, 1/2)

def accuracyCheck(matr, vec, val):
	tmp = True
		for i in range(len(vec)):
			if differenceNorm(matr, vec[ : , i], val[i][i]) > EPS:
				tmp = False
	return tmp

def qrMethod(matr):
	vec = np.eye(4)
	val = matr
	acc = False
	i = 0
	while (acc == False) and (i < MAX_ITER):
		tmp1, tmp2 = al.qr(val)
		vec = np.dot(vec, tmp1)
		val = np.dot(tmp2, tmp1)
		acc = accuracyCheck(matr, vec, val)
		i += 1
		print i, "- th iteration:", "\nFrobenius norm =", frobeniusNorm(vec), "\nDifference norm of first eigvector and first eigvalue =", differenceNorm(matr, vec[ : , 1], val[1][1]), "\n"
	return vec, val

def powerMethod(matr):
	vec = np.array([1., 1., 1., 1.])
	vec = vec/al.norm(vec)
	acc = False
	val = 0
	i = 0
	while (acc == False) and (i < MAX_ITER):
		newVec = np.dot(matr, vec)
		val = al.norm(newVec)/al.norm(vec)
		newVec = newVec/al.norm(newVec)
		if al.norm(newVec - vec) <= EPS:
			acc = True
		i += 1
		vec = newVec
		if (vec[0] <= 0 and np.dot(matr, vec)[0] >= 0) or (vec[0] >= 0 and np.dot(matr, vec)[0] <= 0): val = -val
			return vec, val

matrix = np.array([[6.48, 1.12, 0.95, 1.21],
				   [1.12, 3.94, 1.3, 0.16],
				   [0.95, 1.3, 5.66, 2.1],
				   [1.21, 0.16, 2.1, 5.88]])

print "Matrix:\n", matrix
eigVec, eigVal = qrMethod(matrix)
print "QR method:", "\nEigvectors:\n", eigVec, "\nEigvalues:\n", eigVal
maxEigVec, maxEigVal = powerMethod(matrix)
minEigVec, minEigVal = powerMethod(matrix - maxEigVal*np.eye(4))
print "\nDifference norm of max eigvector and maxeigvalue =", differenceNorm(matrix, maxEigVec, maxEigVal)
print "\nStep method:", "\nMax eigvector:", maxEigVec, "\nMax eigvalue:", maxEigVal, "\nMin eigvector:", minEigVec, "\nMin eigvalue:", minEigVal + maxEigVal