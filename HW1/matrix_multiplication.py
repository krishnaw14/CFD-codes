import sys
import numpy as np 

def initialize_default():
	mat1 = np.array([[3,5] , [4,5]])
	mat2 = np.array([[1,2,3], [4,5,6] ])
	return mat1, mat2

mat1_list = []
mat2_list = []

if len(sys.argv) < 2:
	print("No input file passed, using Default Values")
	mat1, mat2 = initialize_default()

elif len(sys.argv) == 2:
	mat_file = sys.argv[1]
	with open(sys.argv[1], 'r') as f:
		lines = f.readlines()

	mat1_start = lines.index('matrix1\n') + 1
	mat1_end = min(lines.index('matrix2\n'), lines.index('\n')) 
	mat2_start = lines.index('matrix2\n') + 1
	
	for line in lines[mat1_start: mat1_end]:
		row = [float(i) for i in line.split()]
		mat1_list.append(row)

	for line in lines[mat2_start:]:
		row = [float(i) for i in line.split()]
		mat2_list.append(row)

	mat1 = np.array(mat1_list)
	mat2 = np.array(mat2_list)

else:
	print("Please pass only 1 input file - Using Default Values")
	mat1, mat2 = initialize_default()


if mat1.shape[1] != mat2.shape[0]:
	print("Matrices are not compatible for multiplication")

else:
	mat3 = np.zeros((mat1.shape[0], mat2.shape[1]))
	for i in range(mat3.shape[0]):
		for j in range(mat3.shape[1]):
			element = 0
			for k in range(mat2.shape[0]):
				element += mat1[i][k]*mat2[k][j]

			mat3[i][j] = element

	check = np.dot(mat1, mat2)
	print(mat3)
	print("Verifying Answer with numpy matrix multiplication function:", np.array_equal(check, mat3))





	