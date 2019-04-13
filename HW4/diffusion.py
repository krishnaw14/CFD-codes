import numpy as np 
import os 

import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib

# Initialize the grid points as per given in question
def initialize_grid(N, A):
	u_values = np.zeros((N,N))

	x_values = np.linspace(0,20,N)
	y_values = np.linspace(0,20, N)


	for i in range(N):
		for j in range(N):
			x = x_values[i]
			y = y_values[j]

			u_values[i][j] = A*np.exp(-0.5*(x-10)**2 - 0.5*(y-10)**2)

	return u_values

# Add ghost cells to the grid. Implement zero gradient boundary condition.
def add_ghost_cells(u_values, N):
	first_ghost_cell_row = u_values[0]
	last_ghost_cell_row = u_values[-1]

	u_values = np.insert(u_values, 0, first_ghost_cell_row, axis = 0)
	u_values = np.insert(u_values, N, last_ghost_cell_row, axis = 0)

	first_ghost_cell_column = u_values[:,0]
	last_ghost_cell_column = u_values[:,-1]

	u_values = np.insert(u_values, 0, first_ghost_cell_column, axis = 1)
	u_values = np.insert(u_values, N+1, last_ghost_cell_column, axis = 1)

	return u_values

# Solve for u values via finite volume numerical iteration form
def solve_iteration(u_values, N, dt, dx, dy, gamma, simulation_time):

	num_iterations = int(simulation_time/dt)
	print("Simulation Time = {}. Number of iterations = {}".format(simulation_time, num_iterations))

	new_u_values = np.array(u_values)

	fig = plt.figure()
	ax = plt.gca(projection = '3d')
	# axes = Axes3D(fig)
	ax.set_xlim3d(0, 20)
	ax.set_ylim3d(0,20)
	ax.set_zlim3d(0,2)
	X = np.linspace(0,20,N)
	Y = np.linspace(0,20,N)
	X, Y = np.meshgrid(X, Y)

	surf = ax.plot_surface(X, Y, new_u_values[1:N+1, 1:N+1], cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

	ax.set_xlabel('$X$', fontsize=20)
	ax.set_ylabel('$Y$', fontsize=20)
	ax.set_zlabel('$U$', fontsize=20)
	plt.draw()
	plt.pause(0.5)

	for iteration in range(num_iterations):

		f_r = - gamma*(u_values[2:,1:N+1] - u_values[1:N+1,1:N+1])/dx
		f_l = - gamma*(u_values[1:N+1,1:N+1] - u_values[0:N,1:N+1])/dx

		g_r = - gamma*(u_values[1:N+1,2:] - u_values[1:N+1,1:N+1])/dy
		g_l = - gamma*(u_values[1:N+1,1:N+1] - u_values[1:N+1,0:N])/dy

		new_u_values[1:N+1, 1:N+1] = np.array(u_values[1:N+1, 1:N+1] - (dt/dx)*(f_r-f_l) - (dt/dy)*(g_r-g_l))

		new_u_values[0] = np.array(new_u_values[1])
		new_u_values[N+1] = np.array(new_u_values[N])

		new_u_values[:,0] = np.array(new_u_values[:, 1])
		new_u_values[:,N+1] = np.array(new_u_values[:, N])

		u_values = np.array(new_u_values)

		# Change grid after every num_iteration/10 iterations
		if iteration%(num_iterations/10) == 0:
			surf.remove()
			surf = ax.plot_surface(X,Y, u_values[1:N+1, 1:N+1], cmap = cm.coolwarm, 
				linewidth = 0, antialiased = False)
			ax.set_title("Simulating for t = {}s...\n".format(simulation_time), fontsize="15", y=1.08)
			plt.draw()
			plt.pause(0.1)

	# Display and Save the final grid
	surf.remove()
	surf = ax.plot_surface(X, Y, new_u_values[1:N+1, 1:N+1], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
	ax.set_title("3D Plot after t = {}s: ".format(simulation_time))
	plt.savefig(saved_plots_dir + "diffusiont_{}.png".format(simulation_time))

	plt.draw()
	plt.pause(1.5)
	surf.remove()
	plt.close()

	return u_values


N = 101
A = 2
dt = 0.01
dx = 20/(N-1)
dy = 20/(N-1)
gamma = 0.1

time_values = [0,10,20,30,40]
initial_u_values = initialize_grid(N,A)
initial_u_values = add_ghost_cells(initial_u_values, N)

saved_plots_dir = "diffusion_plots/"
if not os.path.exists(saved_plots_dir):
	os.mkdir(saved_plots_dir)

for time in time_values:
	u_values = np.array(solve_iteration(initial_u_values, N, dt, dx, dy, gamma, time))
	fig_2d = plt.figure()
	plt.plot(np.linspace(0,20,N), u_values.diagonal()[1:-1])
	plt.xlabel("x")
	plt.ylabel("U")
	plt.title("Diagonal Plot t = {}s".format(time))
	plt.axis([0,20,0,2])
	plt.savefig(saved_plots_dir+"diagonal_t_{}.png".format(time))
	plt.close()

print("Diagonal Plots have been saved!")




