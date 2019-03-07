import numpy as np 
import matplotlib.pyplot as plt
import os

def initialize_grid(N):
	grid_points = np.linspace(0,1,N)
	u_values = np.zeros(N)
	delta_x = 1/(N-1)
	u_values[0] = 1

	return grid_points, u_values, delta_x


def solve_FTFS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(1,N-1):
		new_values[i] = u_values[i] - cfl*(u_values[i+1] - u_values[i])
	return new_values

def solve_FTBS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(1,N):
		new_values[i] = u_values[i] - cfl*(u_values[i] - u_values[i-1])
	return new_values

def solve_FTCS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(1,N-1):
		new_values[i] = u_values[i] - 0.5*cfl*(u_values[i+1] - u_values[i-1])
	return new_values

def solve_and_plot(scheme_name, solve_scheme, grid_points, u_values, delta_x, simulated_time, cfl, N):
	
	num_iterations = int(simulated_time/(cfl*delta_x))
	print("Number of iterations = ", num_iterations)

	for i in range(num_iterations):
		u_values = np.array(solve_scheme(u_values, cfl, N))

	plt.plot(grid_points, u_values)
	plt.title("Scheme = {} CFL value = {} (t = {}s)".format(scheme_name, cfl, simulated_time))
	plt.xlabel("x")
	plt.ylabel("u(x,t)")
	plt.axis([0,1,min(u_values)/1.2, max(u_values)*1.2])
	plt.savefig(saved_graphs_directory + "Scheme = {} CFL value = {} (t = {}s).png".format(scheme_name, cfl, simulated_time))
	plt.show()

N = 51
grid_points, u_values, delta_x = initialize_grid(N)
simulated_time_values = [0.2, 0.5, 0.7, 1]
cfl_values = [0.4, 0.9, 1.2]

saved_graphs_directory = "saved_graphs_question1/"
if not os.path.exists(saved_graphs_directory):
	os.mkdir(saved_graphs_directory)

# Solve for FTCS
scheme_name = "FTCS"
print("##########################")
print("Solving for FTCS scheme:")
print("##########################\n")
for cfl in cfl_values:
	print("CFL value = ", cfl, "\n")
	for simulated_time in simulated_time_values:
		print("Simulating for t = ", simulated_time)
		solve_and_plot(scheme_name, solve_FTCS, grid_points, u_values, delta_x, simulated_time, cfl, N)
	print("\n")


# Solve for FTBS
scheme_name = "FTBS"
print("##########################")
print("Solving for FTBS scheme:")
print("##########################\n")
for cfl in cfl_values:
	print("CFL value = ", cfl, "\n")
	for simulated_time in simulated_time_values:
		print("Simulating for t = ", simulated_time)
		solve_and_plot(scheme_name, solve_FTBS, grid_points, u_values, delta_x, simulated_time, cfl, N)
	print("\n")

# Solve for FTFS
scheme_name = "FTFS"
print("##########################")
print("Solving for FTFS scheme:")
print("##########################\n")
for cfl in cfl_values:
	print("CFL value = ", cfl, "\n")
	for simulated_time in simulated_time_values:
		print("Simulating for t = ", simulated_time)
		solve_and_plot(scheme_name, solve_FTFS, grid_points, u_values, delta_x, simulated_time, cfl, N)
	print("\n")




