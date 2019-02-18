import numpy as np 
import matplotlib.pyplot as plt

def initialize_matrix(N):
	grid_points = np.zeros((N+1, N+1))

	for i in range(N+1):
		for j in range(N+1):
			x = i/N
			y = j/N
			# print("i = ", i, "j = ",j)

			if i == 0 or j == 0 or i == N or j == N:
				# print("value = ", x**2 - y**2)
				grid_points[i][j] = x**2 - y**2

	return grid_points

def evaluate_residue(grid_points):
	N = np.shape(grid_points)[0] - 1
	residue = 0

	for i in range(N+1):
		for j in range(N+1):
			if i == 0 or j == 0 or i == N or j == N:
				continue
			else:
				value = grid_points[i][j]
				iterate = 0.25*(grid_points[i][j-1] + grid_points[i][j+1] + grid_points[i-1][j] + grid_points[i+1][j])
				residue += (value-iterate)**2

	residue = (residue**0.5)*N
	return residue

def solve_Jacobi(grid_points, max_iterations = 10000):

	error_values = []
	residue_values = []
	num_iteration_values = []

	error_allowed = 2 * np.finfo(np.float64).eps
	error = 100
	N = np.shape(grid_points)[0] - 1
	new_grid_points = np.array(grid_points)
	old_grid_points = np.array(grid_points)
	num_iteration = 1
	residue = evaluate_residue(new_grid_points)
	# while residue >= error_allowed:
	while num_iteration <= max_iterations and error >= error_allowed:

		for i in range(N+1):
			for j in range(N+1):
				if i == 0 or j == 0 or i == N or j == N:
					continue
				else:
					new_grid_points[i][j] = 0.25*(old_grid_points[i-1][j] + old_grid_points[i+1][j] + old_grid_points[i][j-1] + old_grid_points[i][j+1])
					# Oly use past values for iteration in Jacobi method

		error_matrix = (old_grid_points - new_grid_points)**2
		error = (np.sum(error_matrix)**0.5)/N
		residue = evaluate_residue(new_grid_points)
		old_grid_points = np.array(new_grid_points)
		# print("num_iteration:", num_iteration, "error:", residue)

		error_values.append(np.log(error))
		residue_values.append(np.log(residue))
		num_iteration_values.append(num_iteration)
		num_iteration += 1

	return error_values, residue_values


if __name__ == '__main__':
	error_values_jacobi, residue_values_jacobi = solve_Jacobi(initialize_matrix(11))
	plt.plot(np.arange(1, len(residue_values_jacobi)+1), residue_values_jacobi, label = "Residue: N = 11")
	plt.plot(np.arange(1, len(error_values_jacobi)+1), error_values_jacobi, label = "Error: N = 11")
	plt.legend()
	plt.title("Jacobi Solution (Boundary Condition = x^2-y^2)")
	plt.show()









