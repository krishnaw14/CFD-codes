import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib

def initialize_matrix(N):
	grid_points = np.zeros((N+1, N+1))

	for i in range(N+1):
		for j in range(N+1):
			x = i/N
			y = j/N
			# print("i = ", i, "j = ",j)

			if i == 0 or j == 0 or i == N or j == N:
				# print("value = ", x**2 - y**2)
				grid_points[i][j] = np.exp(x-y)

	return grid_points

def solve_GS(grid_points):

	error_values = []
	residue_values = []
	num_iteration_values = []

	error_allowed = 2 * np.finfo(np.float32).eps
	error = 100
	N = np.shape(grid_points)[0] - 1

	X = np.linspace(0,1,N+1)
	Y = np.linspace(0,1,N+1)
	X, Y = np.meshgrid(X, Y)

	new_grid_points = np.array(grid_points)
	old_grid_points = np.array(grid_points)
	num_iteration = 1

	fig = plt.figure()
	ax = fig.gca(projection='3d')

	while error >= error_allowed:

		plot_grid_values = old_grid_points

		for i in range(N+1):
			for j in range(N+1):

				if i == 0 or j == 0 or i == N or j == N:
					continue
				else:
					new_grid_points[i][j] = 0.25*(new_grid_points[i-1][j] + old_grid_points[i+1][j] + new_grid_points[i][j-1] + old_grid_points[i][j+1])

		error_matrix = (old_grid_points - new_grid_points)**2
		error = (np.sum(error_matrix)**0.5)/N
		old_grid_points = np.array(new_grid_points)
		print("num_iteration:", num_iteration, "error:", error)


		error_values.append(np.log(error))
		num_iteration_values.append(num_iteration)


		surf = ax.plot_surface(X, Y, plot_grid_values, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)


		# plt.plot(num_iteration_values, error_values)
		plt.draw() 
		plt.pause(0.05)

		surf.remove()
		num_iteration += 1

# Returns a list of error and residue values for every iteration
def solve_Jacobi(grid_points):

	error_values = []
	residue_values = []
	num_iteration_values = []

	error_allowed = 2 * np.finfo(np.float32).eps
	error = 100
	N = np.shape(grid_points)[0] - 1

	X = np.linspace(0,1,N+1)
	Y = np.linspace(0,1,N+1)
	X, Y = np.meshgrid(X, Y)

	new_grid_points = np.array(grid_points)
	old_grid_points = np.array(grid_points)
	num_iteration = 1

	fig = plt.figure()
	ax = fig.gca(projection='3d')

	while error >= error_allowed:

		plot_grid_values = old_grid_points

		for i in range(N+1):
			for j in range(N+1):

				if i == 0 or j == 0 or i == N or j == N:
					continue
				else:
					new_grid_points[i][j] = 0.25*(old_grid_points[i-1][j] + old_grid_points[i+1][j] + old_grid_points[i][j-1] + old_grid_points[i][j+1])

		error_matrix = (old_grid_points - new_grid_points)**2
		error = (np.sum(error_matrix)**0.5)/N
		old_grid_points = np.array(new_grid_points)
		print("num_iteration:", num_iteration, "error:", error)


		error_values.append(np.log(error))
		num_iteration_values.append(num_iteration)


		surf = ax.plot_surface(X, Y, plot_grid_values, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
		plt.draw() 
		plt.pause(0.05)

		surf.remove()
		num_iteration += 1

if __name__ == '__main__':


	matplotlib.interactive(True)
	solve_GS(initialize_matrix(21))
	plt.show()







