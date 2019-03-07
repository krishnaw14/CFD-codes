import numpy as np
import matplotlib.pyplot as plt

# To initialize the internal grid points with zero and boundary condition
def initialize_matrix(N):
	grid_points = np.zeros((N+1, N+1))
	# grid poinnts go from 0 to N 
	for i in range(N+1):
		for j in range(N+1):
			x = i/N
			y = j/N

			if i == 0 or j == 0 or i == N or j == N:
				# Uncomment the below line and comment the enxt line for 2nd boundary conndition
				# grid_points[i][j] = np.exp(x-y) 
				grid_points[i][j] = x**2 - y**2

	return grid_points


# SOR relaxation scheme
# iterates until error = 2*machine_epsilon or num_iterations <= max_num_iterations
def solve_SOR(grid_points, w, max_num_iterations = 10000):

	error_values = []
	num_iteration_values = []

	error_allowed = 2 * np.finfo(np.float64).eps
	error = 100
	N = np.shape(grid_points)[0] - 1
	new_grid_points = np.array(grid_points)
	old_grid_points = np.array(grid_points)
	num_iteration = 0
	# while error >= error_allowed and num_iteration < max_num_iterations:
	while error>=error_allowed and num_iteration < max_num_iterations:
		for i in range(N+1):
			for j in range(N+1):
				if i == 0 or j == 0 or i == N or j == N:
					continue
				else:
					GS_next_iterate = 0.25*(new_grid_points[i-1][j] + old_grid_points[i+1][j] + new_grid_points[i][j-1] + old_grid_points[i][j+1])
					new_grid_points[i][j] = w*GS_next_iterate + (1-w)*old_grid_points[i][j] #linear combination of new iterate (as per Gauss Seidel) and old grid value.

		error_matrix = (old_grid_points - new_grid_points)**2
		error = (np.sum(error_matrix)**0.5)/N
		old_grid_points = np.array(new_grid_points)
		# print("w:",w, "num_iteration:", num_iteration, "error:", error)
		error_values.append(np.log(error))
		num_iteration_values.append(num_iteration)
		num_iteration += 1
	return error_values


if __name__ == '__main__':
	w_range = np.linspace(0,2,21)
	max_num_iteration_values = [20,40,50,60,100]
	grid_points1 = initialize_matrix(50)

	for max_num_iteration in max_num_iteration_values:
		error_value1 = []
		for w in w_range[1:-1]:
			error_range = solve_SOR(grid_points1, w, max_num_iteration)
			error_value1.append(error_range[-1])

		label = "Number of iterations = " + str(max_num_iteration)
		plt.plot(w_range[1:-1], error_value1, label = label)

	plt.legend()
	plt.title("Error vs w for different grid size (number of iterations = 20)")
	plt.xlabel("w")
	plt.ylabel("Error after iteration")

	plt.show()
