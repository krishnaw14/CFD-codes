import numpy as np 
import matplotlib.pyplot as plt
import os

# To initialize boundary conditions and grid points
def initialize_grid(N):
	grid_points = np.linspace(0,1,N)
	delta_x = 1/(N-1)
	u_values = np.sin(grid_points*2*np.pi)
	u_values[0] = 0
	u_values[-1] = u_values[0] 

	return grid_points, u_values, delta_x

# Defining various numerical schemes
def solve_FTBS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(N):
		new_values[i] = u_values[i] - cfl*(u_values[i] - u_values[i-1])
	# new_values[0] = new_values[-2]
	new_values[0] = new_values[-1]
	return new_values

def solve_FTFS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(1,N-1):
		new_values[i] = u_values[i] - cfl*(u_values[i+1] - u_values[i])
	new_values[0] = new_values[-2]
	new_values[-1] = new_values[1]
	return new_values

def solve_FTCS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(1,N-1):
		new_values[i] = u_values[i] - 0.5*cfl*(u_values[i+1] - u_values[i-1])
	# new_values[-1] = new_values[0]
	new_values[0] = new_values[-2]
	new_values[-1] = new_values[1]
	return new_values

# Solve and plot the propagation of wave for a given condition of numerical sceme, intial and boundary conditions,
# simulated time, CFL value.
# This function will display each graph and save it in a directory
def solve_and_plot(scheme_name, solve_scheme, grid_points, u_values, delta_x, simulated_time, cfl, N):
	
	num_iterations = int(simulated_time/(cfl*delta_x))
	print("Number of iterations = ", num_iterations)
	print("Saving the waveform at the end of simulated time")

	for i in range(num_iterations):
		u_values = np.array(solve_scheme(u_values, cfl, N))

	plt.plot(grid_points, u_values)
	plt.title("Scheme = {} CFL value = {} (t = {}s)".format(scheme_name, cfl, simulated_time))
	plt.xlabel("x")
	plt.ylabel("u(x,t)")
	# plt.pause(0.0001)
	# 	if i != (num_iterations-1):
	# 		plt.clf()
	# plt.axis([0,1,-1,1])
	# plt.show()
	plt.savefig(saved_graphs_directory + "Scheme = {} CFL value = {} (t = {}s).png".format(scheme_name, cfl, simulated_time))
	plt.pause(0.5)
	plt.clf()


N = 101
cfl = 0.5
simulated_time_values = [0, 1, 1.5, 3, 4]

# Intialize domain and initial and boundary conditions
grid_points, u_values, delta_x = initialize_grid(N)

# Define directory to save all the graphs
saved_graphs_directory = "saved_graphs_question2/"
if not os.path.exists(saved_graphs_directory):
	os.mkdir(saved_graphs_directory)

# Plot initial boundary conditions
plt.plot(grid_points, u_values)
plt.title("Initial Boundary Conditions")
plt.xlabel("x")
plt.ylabel("u(x,t)")
# plt.axis([0,1,min(u_values)/1.2, max(u_values)*1.2])
plt.savefig(saved_graphs_directory + "InitialBC.png")
plt.pause(1)
plt.clf()


# Solve for FTCS
scheme_name = "FTCS"
print("##########################")
print("Solving for FTCS scheme:")
print("##########################\n")
print("CFL value = ", cfl, "\n")
for simulated_time in simulated_time_values:
	print("Simulating for t = ", simulated_time)
	solve_and_plot(scheme_name, solve_FTCS, grid_points, u_values, delta_x, simulated_time, cfl, N)
	print("\n")

# # # Solve for FTFS
scheme_name = "FTFS"
print("##########################")
print("Solving for FTFS scheme:")
print("##########################\n")
print("CFL value = ", cfl, "\n")
for simulated_time in simulated_time_values:
	print("Simulating for t = ", simulated_time)
	solve_and_plot(scheme_name, solve_FTFS, grid_points, u_values, delta_x, simulated_time, cfl, N)
	print("\n")

# # Solving for FTBS scheme
scheme_name = "FTBS"
print("##########################")
print("Solving for FTBS scheme:")
print("##########################\n")
print("CFL value = ", cfl, "\n")
for simulated_time in simulated_time_values:
	print("Simulating for t = ", simulated_time)
	solve_and_plot("FTBS", solve_FTBS, grid_points, u_values, delta_x, simulated_time, cfl, N)
	print("\n")





