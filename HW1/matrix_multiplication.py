# Check README.md for instruction to run.
# Check input_array.txt for the format in which the matrices need to be input.

import sys
import numpy as np 

# Default initialization of the matrices in case the command line argument of matrix input files in not passed
def initialize_default():
	mat1 = np.array([[3,5] , [4,5]])
	mat2 = np.array([[1,2,3], [4,5,6] ])
	return mat1, mat2

mat1_list = []
mat2_list = []

# Check if a matrix input file is passed
if len(sys.argv) < 2:
	print("No input file passed, using Default Values")
	mat1, mat2 = initialize_default()

# Read the matrix input file, store the matrices as two distinct numpy 2D arrays
elif len(sys.argv) == 2:
	mat_file = sys.argv[1] # File Path
	with open(sys.argv[1], 'r') as f: # Read the file content from file path
		lines = f.readlines()

	mat1_start = lines.index('matrix1\n') + 1 # Where matrix 1 starts
	mat1_end = min(lines.index('matrix2\n'), lines.index('\n')) # Where matrix 1 ends. It is assumed that matrix 1 ends at blank line or where matrix 2 starts.
	mat2_start = lines.index('matrix2\n') + 1 # Where Matrix 2 starts. Matrix 2 is assumed to end at the end of the file.
	
	# Read the lines from file, split the space seprated numbers and store in list.
	for line in lines[mat1_start: mat1_end]: 
		row = [float(i) for i in line.split()]
		mat1_list.append(row)

	for line in lines[mat2_start:]:
		row = [float(i) for i in line.split()]
		mat2_list.append(row)

	# Convert the list of lists to 2D numpy array
	mat1 = np.array(mat1_list) 
	mat2 = np.array(mat2_list)

else:
	print("Please pass only 1 input file - Using Default Values")
	mat1, mat2 = initialize_default()

# Check multiplication compatibility of the two matrices
if mat1.shape[1] != mat2.shape[0]:
	print("Matrices are not compatible for multiplication")

# By matrix multiplication definition (C= AB, where A is (mxn) and B is a (nxm) matrix):
# c_{ij} = \Sigma_{k=1}^{n}(a_{ik}b_{kj}) where a_{ik} element of A in ith row and kth column and likewise for b_{kj}
else:
	mat3 = np.zeros((mat1.shape[0], mat2.shape[1])) # Initialize the matrix multiplication product
	for i in range(mat3.shape[0]):
		for j in range(mat3.shape[1]):
			element = 0
			for k in range(mat2.shape[0]):
				element += mat1[i][k]*mat2[k][j]

			mat3[i][j] = element

	check = np.dot(mat1, mat2) # Exact answer is found using in-built funnction in numpy
	print(mat3)
	print("Verifying Answer with numpy matrix multiplication function:", np.array_equal(check, mat3)) # Verify the answer





	