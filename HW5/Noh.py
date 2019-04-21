import os
import numpy as np 
import matplotlib.pyplot as plt 

def initialize_grid(N, var, x_values):
	grid_values = np.zeros((N+2, 1))

	left_bc_values = {
	"density": 1,
	"velocity": 1,
	"pressure": 1e-6
	}
	right_bc_values = {
	"density": 1,
	"velocity": -1,
	"pressure": 1e-6
	}

	for i in range(1,N+1):
		x = x_values[i-1]
		if x<=0.5:
			grid_values[i,0] = left_bc_values[var]
		else:
			grid_values[i,0] = right_bc_values[var]

	# Add Ghost Cells
	# grid_values = np.insert(grid_values, N, grid_values[-1,:], axis = 0)
	# grid_values = np.insert(grid_values, 0, grid_values[0,:], axis = 0)
	grid_values[0] = grid_values[1]
	grid_values[-1] = grid_values[-2]


	return grid_values


def solve_iteration(x_values, density_values, momentum_values, energy_values, N, dt, dx, gamma, simulation_time, scheme_name):
	num_iterations = int(simulation_time/dt)
	
	print("Scheme = {}. N = {}. Simulation Time = {}. Number of iterations = {}".format(scheme_name, N, simulation_time, num_iterations))

	new_density_values = np.array(density_values)
	new_momentum_values = np.array(momentum_values)
	new_energy_values = np.array(energy_values)

	for iteration in range(num_iterations):

		velocity_values = np.array(momentum_values/density_values)
		pressure_values = (gamma-1)*(energy_values - 0.5*momentum_values*momentum_values/density_values)

		if scheme_name == "Rusonov":	
			Lambda_R = np.maximum( np.abs(velocity_values[1:N+1])+1, np.abs(velocity_values[2:N+2])+1 ) 
			Lambda_L = np.maximum( np.abs(velocity_values[1:N+1])+1, np.abs(velocity_values[0:N])+1 ) 
		elif scheme_name == "LF":
			Lambda_R = np.array(np.abs(velocity_values[1:N+1])  )
			Lambda_L = np.array(np.abs(velocity_values[1:N+1]))

		# Mass Conservation
		density_flux_values = np.array(momentum_values)
		density_flux_R = 0.5*(density_flux_values[1:N+1] + density_flux_values[2:N+2]) - 0.5*Lambda_R*(density_values[2:N+2] - density_values[1:N+1])
		density_flux_L = 0.5*(density_flux_values[1:N+1] + density_flux_values[0:N]) - 0.5*Lambda_L*(density_values[1:N+1] - density_values[0:N])

		new_density_values[1:N+1] = np.array(density_values[1:N+1] - (dt/dx)*(density_flux_R - density_flux_L))

		# Momentum Conservation
		momentum_flux_values = (momentum_values*momentum_values/density_values) + pressure_values
		momentum_flux_R = 0.5*(momentum_flux_values[1:N+1] + momentum_flux_values[2:N+2]) - 0.5*Lambda_R*(momentum_values[2:N+2] - momentum_values[1:N+1])
		momentum_flux_L = 0.5*(momentum_flux_values[1:N+1] + momentum_flux_values[0:N]) - 0.5*Lambda_L*(momentum_values[1:N+1] - momentum_values[0:N])

		new_momentum_values[1:N+1] = np.array(momentum_values[1:N+1] - (dt/dx)*(momentum_flux_R - momentum_flux_L))


		# Energy Convervation
		energy_flux_values = (momentum_values/density_values)*(energy_values + pressure_values)
		energy_flux_R = 0.5*(energy_flux_values[1:N+1] + energy_flux_values[2:N+2]) - 0.5*Lambda_R*(energy_values[2:N+2] - energy_values[1:N+1])
		energy_flux_L = 0.5*(energy_flux_values[1:N+1] + energy_flux_values[0:N]) - 0.5*Lambda_L*(energy_values[1:N+1] - energy_values[0:N])

		new_energy_values[1:N+1] = np.array(energy_values[1:N+1] - (dt/dx)*(energy_flux_R - energy_flux_L))

		# Apply Boundary Conditions
		new_density_values[0] = new_density_values[1]
		new_density_values[-1] = new_density_values[-2]

		new_momentum_values[0] = new_momentum_values[1]
		new_momentum_values[-1] = new_momentum_values[-2]

		new_energy_values[0] = new_energy_values[1]
		new_energy_values[-1] = new_energy_values[-2]

		# Update for next iteration
		density_values = np.array(new_density_values)
		momentum_values = np.array(new_momentum_values)
		energy_values = np.array(new_energy_values)

	pressure_values = (gamma-1)*(energy_values - 0.5*momentum_values*momentum_values/density_values)
	velocity_values = np.array(momentum_values/density_values)

	plt.plot(x_values, density_values[1:-1])
	plt.title("Noh - {}: Density Variation (N = {})".format(scheme_name, N-1))
	plt.xlabel("x")
	plt.ylabel("Density")
	plt.savefig("{}density_N{}_{}.png".format(saved_graphs_directory, N, scheme_name))
	plt.pause(1)
	plt.close()

	plt.plot(x_values, velocity_values[1:-1])
	plt.title("Noh - {}: Velocity Variation (N = {})".format(scheme_name, N-1))
	plt.xlabel("x")
	plt.ylabel("Velocity")
	plt.savefig("{}velocity_N{}_{}.png".format(saved_graphs_directory, N, scheme_name))
	plt.pause(1)
	plt.close()

	plt.plot(x_values, pressure_values[1:-1])
	plt.title("Noh - {}: Pressure Variation (N = {})".format(scheme_name, N-1))
	plt.xlabel("x")
	plt.ylabel("Pressure")
	plt.savefig("{}pressure_N{}_{}.png".format(saved_graphs_directory, N, scheme_name))
	plt.pause(1)
	plt.close()



N_values = [101, 201, 401,801]
cfl = 0.3
a = 374.17
simulation_time = 1
gamma = 5.0/3

saved_graphs_directory = "Nohgraphs/"
if not os.path.exists(saved_graphs_directory):
	os.mkdir(saved_graphs_directory)

for N in N_values:
	x_values = np.linspace(0,1,N)
	dx = 1/(N-1)
	dt = cfl*dx/a

	density_values = np.array(initialize_grid(N, "density", x_values))
	velocity_values = np.array(initialize_grid(N, "velocity", x_values))
	pressure_values = np.array(initialize_grid(N, "pressure", x_values))


	momentum_values = np.array(density_values*velocity_values)
	energy_values = np.array(0.5*density_values*velocity_values*velocity_values + pressure_values/(gamma-1))


	solve_iteration(x_values, density_values, momentum_values, energy_values, N, dt, dx, gamma, simulation_time, "LF")
	solve_iteration(x_values, density_values, momentum_values, energy_values, N, dt, dx, gamma, simulation_time, "Rusanov")





