import numpy as np 
import os 

import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib

def initialize_grid(N, A):
	u_values = np.zeros((N,N))

	x_values = np.linspace(0,20,N)
	y_values = np.linspace(0,20, N)


	for i in range(N):
		for j in range(N):
			x = x_values[i]
			y = y_values[j]

			u_values[i][j] = A*np.exp(-0.5*(x-5)**2 - 0.5*(y-5)**2)

	return u_values

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


def solve_lax_friedrichs(u_values, N, dt, dx, dy, simulation_time):

	# print(u_values)

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

	# Lambda = 1*(1*dt/dx)
	Lambda = 1

	surf = ax.plot_surface(X, Y, new_u_values[1:N+1, 1:N+1], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
	plt.draw()
	plt.pause(0.5)

	for iteration in range(num_iterations):

		for i in range(1,N+1):
			for j in range(1,N+1):

				f_r = 0.5*(u_values[i+1][j] + u_values[i][j]) - 0.5*Lambda*(u_values[i+1][j] - u_values[i][j])
				f_l = 0.5*(u_values[i][j] + u_values[i-1][j]) - 0.5*Lambda*(u_values[i][j] - u_values[i-1][j])

				g_r = 0.5*(u_values[i][j+1] + u_values[i][j]) - 0.5*Lambda*(u_values[i][j+1] - u_values[i][j])
				g_l = 0.5*(u_values[i][j] + u_values[i][j-1]) - 0.5*Lambda*(u_values[i][j] - u_values[i][j-1])

				new_u_values[i][j] = u_values[i][j] - (dt/dx)*(f_r-f_l) - (dt/dy)*(g_r-g_l)

		new_u_values[0] = new_u_values[1]
		new_u_values[N+1] = new_u_values[N]

		new_u_values[:,0] = new_u_values[:, 1]
		new_u_values[:,N+1] = new_u_values[:, N]

		u_values = np.array(new_u_values)

		# if iteration%10 == 0:
	surf.remove()
	surf = ax.plot_surface(X, Y, new_u_values[1:N+1, 1:N+1], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

	print(np.max(u_values), np.unravel_index(u_values.argmax(), u_values.shape))

			# u_values = np.array(new_u_values)

		# print(iteration)
		# print(np.max(u_values), np.unravel_index(u_values.argmax(), u_values.shape))

	plt.draw()
	plt.show()
	surf.remove()

# def solve_upwind():

# def solve_ftcs_2


N = 101
A = 2
dt = 0.001
dx = 20/(N-1)
dy = 20/(N-1)

time_values = [10]
initial_u_values = initialize_grid(N,A)
initial_u_values = add_ghost_cells(initial_u_values, N)
# print(np.linspace(0,20,N)[25])

for time in time_values:
	solve_lax_friedrichs(initial_u_values, N, dt, dx, dy, time)