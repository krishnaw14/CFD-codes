import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib
# from SOR import solve_SOR

def initialize_matrix(N):
	grid_points = np.zeros((N+1, N+1))

	for i in range(N+1):
		for j in range(N+1):
			x = i/N
			y = j/N

			if i == 0 or j == 0 or i == N or j == N:
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

# Returns a list of error and residue values for every iteration
def solve_GS(grid_points, max_iterations = 10000):

	error_values = []
	residue_values = []
	num_iteration_values = []

	error_allowed = 2 * np.finfo(np.float32).eps
	error = 100
	N = np.shape(grid_points)[0] - 1
	new_grid_points = np.array(grid_points)
	old_grid_points = np.array(grid_points)
	num_iteration = 1
	residue = evaluate_residue(new_grid_points)
	# while residue >= error_allowed:
	while num_iteration <= 5000 and error >= error_allowed:

		for i in range(N+1):
			for j in range(N+1):
				if i == 0 or j == 0 or i == N or j == N:
					continue
				else:
					new_grid_points[i][j] = 0.25*(new_grid_points[i-1][j] + old_grid_points[i+1][j] + new_grid_points[i][j-1] + old_grid_points[i][j+1])
					# Take new grid values for previous positions

		error_matrix = (old_grid_points - new_grid_points)**2
		error = (np.sum(error_matrix)**0.5)/N
		residue = evaluate_residue(new_grid_points)
		old_grid_points = np.array(new_grid_points)

		error_values.append(np.log(error))
		residue_values.append(np.log(residue))
		num_iteration_values.append(num_iteration)
		num_iteration += 1

	return error_values, residue_values

if __name__ == '__main__':
	error_values_gs, residue_values_gs = solve_GS(initialize_matrix(11), 10000)
	plt.plot(np.arange(1, len(residue_values_gs)+1), residue_values_gs, label = "Residue: N = 11")
	plt.plot(np.arange(1, len(error_values_gs)+1), error_values_gs, label = "Error: N = 11")
	plt.legend()
	plt.title("Gauss Seidel Solution (Boundary Condition = x^2-y^2)")
	plt.show()






