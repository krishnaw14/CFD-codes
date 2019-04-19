import os
import numpy as np 
import matplotlib.pyplot as plt 

def initialize_grid(N):
	U_values = np.zeros((N, 3))

	for i in range(N):
		x = i/N

		if x<0.3:
			U_values[i,0] = 1
			U_values[i:1] = 0.75
			U_values[i:2] = 1
		else:
			U_values[i,0] = 0.125
			U_values[i:1] = 0
			U_values[i:2] = 0.1

	# Add Ghost Cells
	U_values = np.insert(U_values,N, U_values[-1,:], axis = 0)
	U_values = np.insert(U_values, 0, U_values[0,:], axis = 0)

	return U_values


def solve_iteration(U_values, N, dt, dx, simulation_time):
	num_iterations = int(simulation_time/dt)
	x_values = np.linspace(0,1,N)
	print("Simulation Time = {}. Number of iterations = {}".format(simulation_time, num_iterations))

	new_U_values = np.array(U_values)

	for iteration in range(num_iterations):

		for i in range(1,N+1):

			A = np.array([[U_values[i][1], U_values[i][0], 0], [0, U_values[i][1], 1/U_values[i][0]], [0, 1.4*U_values[i][2], U_values[i][1]]])

			new_U_values[i,:] = 0.5*(U_values[i-1,:]+U_values[i+1,:]) - (dt/2*dx)*(np.dot(A, U_values[i+1,:]) - np.dot(A, U_values[i-1,:]) )

		new_U_values[0,:] = new_U_values[1,:]
		new_U_values[-1,:] = new_U_values[-2,:]

		U_values = np.array(new_U_values)

		# plt.plot(x_values, new_U_values[1:-1,0])
		# plt.title("Density Variation")
		# plt.pause(0.05)
		# plt.clf()

	plt.plot(x_values, new_U_values[1:-1,0])
	plt.axis([0,1,0,1])
	plt.title("Density Variation")
	plt.show()





N = 101
dx = 1/(N-1)
cfl = 0.3
a = 374
dt = cfl*dx/a
simulation_time = 0.2

U_values = initialize_grid(N)
print(U_values.shape)
solve_iteration(U_values, N, dt, dx, simulation_time)
