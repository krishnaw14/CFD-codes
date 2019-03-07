import numpy as np 
import matplotlib.pyplot as plt

def solve_FTFS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(0,N-1):
		new_values[i] = u_values[i] - cfl*(u_values[i+1] - u_values[i])
	new_values[-1] = new_values[0]
	return new_values

def solve_FTBS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(1,N):
		new_values[i] = u_values[i] - cfl*(u_values[i] - u_values[i-1])
	new_values[0] = new_values[-1]
	return new_values

def solve_FTCS(u_values, cfl, N):
	new_values = np.array(u_values)
	for i in range(1,N-1):
		new_values[i] = u_values[i] - 0.5*cfl*(u_values[i+1] - u_values[i-1])
	return new_values


N = 101
cfl = 0.5
simulated_time = 1.1

# Intialize domain and initial and boundary conditions
grid_points = np.linspace(-1,1,N)
delta_x = 2/(N-1)
# u_values = np.zeros(N)
u_values = np.sin(grid_points*2*np.pi)
u_values[0] = 0
u_values[-1] = u_values[0] 


num_iterations = int(simulated_time/(cfl*delta_x))
print("Simulating for", num_iterations, "number of iterations")

for i in range(num_iterations):
	plt.plot(grid_points, u_values)
	plt.axis([-1,1,-1.2, 1.2])
	u_values = np.array(solve_FTBS(u_values, cfl, N))
	print(max(u_values))
	plt.pause(0.005)
	plt.clf()

# plt.plot(grid_points, u_values)
# plt.title("Scheme = FTCS, CFL value = {} (t = {}s)".format(cfl, simulated_time))
# plt.xlabel("x")
# plt.ylabel("u(x,t)")
# plt.axis([0,1,0, max(u_values)*1.2])
# plt.show()
