import numpy as np 
import os 

import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib

def initialize_grid(N, A):
	u_values = np.zeros((N,N))

	x_values = np.linspace(0,15,N)
	y_values = np.linspace(0,15,N)


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


def solve_iteration(u_values, N, dt, dx, dy, nu, Lambda, simulation_time, scheme_name):

	num_iterations = int(simulation_time/dt)
	print("Simulating for t = {}s. Number of iterations = {}".format(simulation_time, num_iterations))

	new_u_values = np.array(u_values)

	fig = plt.figure()
	ax = plt.gca(projection = '3d')
	# axes = Axes3D(fig)
	ax.set_xlim3d(0, 15)
	ax.set_ylim3d(0,15)
	ax.set_zlim3d(0,2)
	X = np.linspace(0,15,N)
	Y = np.linspace(0,15,N)
	X, Y = np.meshgrid(X, Y)

	plt.tight_layout() 
	surf = ax.plot_surface(X, Y, new_u_values[1:N+1, 1:N+1], cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
	ax.set_xlabel('$X$', fontsize=20)
	ax.set_ylabel('$Y$', fontsize=20)
	ax.set_zlabel('$U$', fontsize=20)
	plt.draw()
	plt.pause(0.5)

	for iteration in range(num_iterations):

		if scheme_name == "Lax-Friedrich":
			Lambda = u_values[1:N+1,1:N+1]

		f_r = 0.25*(u_values[2:,1:N+1]**2 + u_values[1:N+1,1:N+1]**2) -nu*(u_values[2:,1:N+1] - u_values[1:N+1,1:N+1])/dx  - 0.5*Lambda*(u_values[2:,1:N+1] - u_values[1:N+1,1:N+1])
		f_l = 0.25*(u_values[1:N+1,1:N+1]**2 + u_values[0:N,1:N+1]**2) -nu*(u_values[1:N+1,1:N+1] - u_values[0:N,1:N+1])/dx  - 0.5*Lambda*(u_values[1:N+1,1:N+1] - u_values[0:N,1:N+1])

		g_r = 0.25*(u_values[1:N+1,2:]**2 + u_values[1:N+1,1:N+1]**2) -nu*(u_values[1:N+1,2:] - u_values[1:N+1,1:N+1])/dy - 0.5*Lambda*(u_values[1:N+1,2:] - u_values[1:N+1,1:N+1])
		g_l = 0.25*(u_values[1:N+1,1:N+1]**2 + u_values[1:N+1,0:N]**2) -nu*(u_values[1:N+1,1:N+1] - u_values[1:N+1,0:N])/dy - 0.5*Lambda*(u_values[1:N+1,1:N+1] - u_values[1:N+1,0:N])

		new_u_values[1:N+1, 1:N+1] = np.array(u_values[1:N+1, 1:N+1] - (dt/dx)*(f_r-f_l) - (dt/dy)*(g_r-g_l))

		new_u_values[0] = new_u_values[1]
		new_u_values[N+1] = new_u_values[N]

		new_u_values[:,0] = new_u_values[:, 1]
		new_u_values[:,N+1] = new_u_values[:, N]

		u_values = np.array(new_u_values)

		if iteration%(num_iterations/10) == 0:

			surf.remove()
			plt.tight_layout() 
			surf = ax.plot_surface(X, Y, new_u_values[1:N+1, 1:N+1], cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
			ax.set_title("Simulating for t = {}s: Scheme: {}, ν: {}\n".format(simulation_time, scheme_name, nu), fontsize="15", y=1.08)
			plt.draw()
			plt.pause(0.1)

	surf.remove()
	plt.tight_layout() 
	surf = ax.plot_surface(X, Y, u_values[1:N+1, 1:N+1], cmap = cm.coolwarm, 
		linewidth = 0, antialiased=False)
	ax.set_title("3D Plot after t = {}s: Scheme: {}, ν: {}\n".format(simulation_time, scheme_name, nu))
	plt.draw()
	plt.savefig(saved_plots_dir+"burger_{}_t_{}_nu_{}.png".format(scheme_name, simulation_time, nu))
	plt.pause(2)
	surf.remove()
	print("Plot saved!")
	plt.close()

	return u_values


N = 101
A = 2
dt = 0.001
dx = 15/(N-1)
dy = 15/(N-1)
nu_values = [0,0.02,0.04]


time_values = [0,5,15,20,25]
initial_u_values = initialize_grid(N,A)
initial_u_values = add_ghost_cells(initial_u_values, N)
saved_plots_dir = "burger_plots/"
if not os.path.exists(saved_plots_dir):
	os.mkdir(saved_plots_dir)

print("Solving For FTBS... ")
Lambda = 1
for time in time_values:
	for nu in nu_values:
		print("nu =", nu)
		u_values = solve_iteration(initial_u_values, N, dt, dx, dy, nu, Lambda, time, "FTBS")
		fig_2d = plt.figure()
		plt.plot(np.linspace(0,15,N), u_values.diagonal()[1:-1])
		plt.xlabel("x")
		plt.ylabel("U")
		plt.title("Main Diagonal Plot t = {}s. Scheme: {}, ν: {}".format(time, "FTBS", nu))
		plt.savefig(saved_plots_dir+"burger_diagonal_{}_t_{}_nu_{}.png".format("FTBS", time, nu))
		plt.close()

		fig_2d = plt.figure()
		plt.plot(np.linspace(0,15,N), np.diag(np.fliplr(u_values))[1:-1])
		plt.xlabel("x")
		plt.ylabel("U")
		plt.title("Opposite Diagonal Plot t = {}s. Scheme: {}, ν: {}".format(time, "FTBS", nu))
		plt.savefig(saved_plots_dir+"burger_other_diagonal_{}_t_{}_nu_{}.png".format("FTBS", time, nu))
		plt.close()

print("Diagonal Plots have been generated!\n\n")

print("Solving For Lax Friedrich... ")
Lambda = 0 # Lambda is initialized in solve_iteration function for this scheme. Here 0 is just a garbage value.
for time in time_values:
	for nu in nu_values:
		print("nu =", nu)
		u_values = solve_iteration(initial_u_values, N, dt, dx, dy, nu, Lambda, time, "Lax-Friedrich")
		fig_2d = plt.figure()
		plt.plot(np.linspace(0,15,N), u_values.diagonal()[1:-1])
		plt.xlabel("x")
		plt.ylabel("U")
		plt.title("Main Diagonal Plot t = {}s. Scheme: {}, ν: {}".format(time, "Lax-Friedrich", nu))
		plt.savefig(saved_plots_dir+"burger_diagonal_{}_t_{}_nu_{}.png".format("Lax-Friedrich", time, nu))
		plt.close()

		fig_2d = plt.figure()
		plt.plot(np.linspace(0,15,N), np.diag(np.fliplr(u_values))[1:-1])
		plt.xlabel("x")
		plt.ylabel("U")
		plt.title("Other Diagonal Plot t = {}s. Scheme: {}, ν: {}".format(time, "Lax-Friedrich", nu))
		plt.savefig(saved_plots_dir+"burger_other_diagonal_{}_t_{}_nu_{}.png".format("Lax-Friedrich", time, nu))
		plt.close()

print("Diagonal Plots have been generated!\n\n")

print("Solving For FTCS2... ")
Lambda = dt/dx
for time in time_values:
	for nu in nu_values:
		print("nu =", nu)
		u_values = solve_iteration(initial_u_values, N, dt, dx, dy, nu, Lambda, time, "FTCS2")
		fig_2d = plt.figure()
		plt.plot(np.linspace(0,15,N), u_values.diagonal()[1:-1])
		plt.xlabel("x")
		plt.ylabel("U")
		plt.title("Main Diagonal Plot t = {}s. Scheme: {}, ν: {}".format(time, "FTCS2", nu))
		plt.savefig(saved_plots_dir+"burger_diagonal_{}_t_{}_nu_{}.png".format("FTCS2", time, nu))
		plt.close()

		fig_2d = plt.figure()
		plt.plot(np.linspace(0,15,N), np.diag(np.fliplr(u_values))[1:-1])
		plt.xlabel("x")
		plt.ylabel("U")
		plt.title("Other Diagonal Plot t = {}s. Scheme: {}, ν: {}".format(time, "FTCS2", nu))
		plt.savefig(saved_plots_dir+"burger_other_diagonal_{}_t_{}_nu_{}.png".format("FTCS2", time, nu))
		plt.close()



print("Diagonal Plots have been generated!")



	
