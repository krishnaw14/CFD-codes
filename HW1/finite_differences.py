import numpy as np 
import matplotlib.pyplot as plt 
import os

def f(x): # Function whose derivative we need to calculate
	return np.sin(x)

def Df(x): # Exact derivative of f. This is used to compute error of the finite differences methods.
	return np.cos(x)

############################################
# Functions to calculate forward (1st, 2nd and 3rd Order), backward(1st, 2nd and 3rd Order) and central(2nd and 4th Order) 
# difference based derivatives of a function f at x 
# with h=dx as the differnce between x_i and x_i+1.
# The formulas for first, second and third order have been derived in the report.
############################################

def forward_difference(f, x, dx):

	# 1st order
	derivative_forward_1 = (f(x+dx) - f(x))/dx

	# 2nd order
	derivative_forward_2 = (-f(x+2*dx) + 4*f(x+dx) - 3*f(x))/(2*dx)
	
	# 3rd order
	derivative_forward_3 = (2*f(x+3*dx) - 9*f(x+2*dx) + 18*f(x+dx) - 11*f(x))/(6*dx)

	return derivative_forward_1, derivative_forward_2, derivative_forward_3

def backward_difference(f, x, dx):

	# 1st order
	derivative_backward_1 = (f(x) - f(x-dx))/dx

	# 2nd order
	derivative_backward_2 = (3*f(x) - 4*f(x-dx) + f(x-2*dx))/(2*dx)
	
	# 3rd order
	derivative_backward_3 = (4*f(x) - 7*f(x-dx) + 4*f(x-2*dx) - f(x-3*dx))/(2*dx)

	return derivative_backward_1, derivative_backward_2, derivative_backward_3

def central_difference(f, x, dx):

	# 2nd order
	derivative_central_2 = (f(x+dx) - f(x-dx))/(2*dx)

	# 4th order
	derivative_central_4 = (-f(x+2*dx) + 8*f(x+dx) - 8*f(x-dx) + f(x-2*dx))/(12*dx)

	return derivative_central_2, derivative_central_4


saved_graphs_dir = "Graphs-Finite_Differences/" # Folder to save the graphs
if not os.path.exists(saved_graphs_dir):
	os.mkdir(saved_graphs_dir)

# Define the dictionary to store errors of forward, backward and central difference methods for different orders
forward_difference_error = {
	"1st Order" : [],
	"2nd Order": [],
	"3rd Order": []
}
backward_difference_error = {
	"1st Order" : [],
	"2nd Order": [],
	"3rd Order": []
}
central_difference_error = {
	"2nd Order": [],
	"4th Order": []
}

x = 1 # Value whose derivative is to be evaluated
dx_range = [] # Store the range of dx values. Used to plot the error values vs dx. 
exact_value = Df(x) # Exact value used to compute error. 

for i in range(10):
	dx = 1/(2**i) # Half the value of dx after every iteration
	dx_range.append(dx)
	f1, f2, f3 = forward_difference(f, x, dx)
	# print((f1-exact_value)/exact_value)
	forward_difference_error["1st Order"].append(abs(f1-exact_value)/exact_value)
	forward_difference_error["2nd Order"].append(abs(f2-exact_value)/exact_value)
	forward_difference_error["3rd Order"].append(abs(f3-exact_value)/exact_value)

	b1, b2, b3 = backward_difference(f, x, dx)
	backward_difference_error["1st Order"].append(abs(b1-exact_value)/exact_value)
	backward_difference_error["2nd Order"].append(abs(b2-exact_value)/exact_value)
	backward_difference_error["3rd Order"].append(abs(b3-exact_value)/exact_value)

	c2, c4 = central_difference(f, x, dx)
	central_difference_error["2nd Order"].append(abs(c2-exact_value)/exact_value)
	central_difference_error["4th Order"].append(abs(c4-exact_value)/exact_value)

############################################
# Plot Error vs dx graphs in Normal scaling
############################################

plt.plot(dx_range, forward_difference_error["1st Order"])
plt.plot(dx_range, forward_difference_error["2nd Order"])
plt.plot(dx_range, forward_difference_error["3rd Order"])
plt.legend(["1st Order", "2nd Order", "3rd Order"])
plt.title("Forward Difference (normal scale)")
plt.xlabel("dx")
plt.ylabel("error")
plt.savefig(saved_graphs_dir + "normal-scale-forward_difference.png")
plt.show()

plt.plot(dx_range, backward_difference_error["1st Order"])
plt.plot(dx_range, backward_difference_error["2nd Order"])
plt.plot(dx_range, backward_difference_error["3rd Order"])
plt.legend(["1st Order", "2nd Order", "3rd Order"])
plt.title("Backward Difference (normal scale)")
plt.xlabel("dx")
plt.ylabel("error")
plt.savefig(saved_graphs_dir + "normal-scale-backward_difference.png")
plt.show()

plt.plot(dx_range, central_difference_error["2nd Order"])
plt.plot(dx_range, central_difference_error["4th Order"])
plt.legend(["2nd Order", "4th Order"])
plt.title("Central Difference (normal scale)")
plt.xlabel("dx")
plt.ylabel("error")
plt.savefig(saved_graphs_dir + "normal-scale-central_difference.png")
plt.show()

plt.plot(dx_range, forward_difference_error["2nd Order"])
plt.plot(dx_range, backward_difference_error["2nd Order"])
plt.plot(dx_range, central_difference_error["2nd Order"])
plt.legend(["forward", "backward", "central"])
plt.title("Forward vs Backward Vs Central (2nd Order- Normal Scale)")
plt.xlabel("dx")
plt.ylabel("error")
plt.savefig(saved_graphs_dir + "normal-scale-second_order.png")
plt.show()

plt.plot(dx_range, forward_difference_error["1st Order"])
plt.plot(dx_range, forward_difference_error["2nd Order"])
plt.plot(dx_range, forward_difference_error["3rd Order"])
plt.plot(dx_range, backward_difference_error["1st Order"])
plt.plot(dx_range, backward_difference_error["2nd Order"])
plt.plot(dx_range, backward_difference_error["3rd Order"])
plt.plot(dx_range, central_difference_error["2nd Order"])
plt.plot(dx_range, central_difference_error["4th Order"])
plt.legend(["Forward-1st Order", "Forward-2nd Order", "Forward-3rd Order", "Backward-1st Order", 
	"Backward-1st Order", "Backward-1st Order", "Backward-1st Order", "Backward-1st Order"])
plt.title("Forward vs Central vs Backward (Normal Scale)")
plt.xlabel("dx")
plt.ylabel("error")
plt.savefig(saved_graphs_dir + "normal-scale-all.png")
plt.show()


############################################
# Plot Error vs dx graphs in log-log scaling
############################################
plt.plot(np.log2(dx_range), np.log2(forward_difference_error["1st Order"]))
plt.plot(np.log2(dx_range), np.log2(forward_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(forward_difference_error["3rd Order"]))
plt.legend(["1st Order", "2nd Order", "3rd Order"])
plt.title("Forward Difference (log-log scale)")
plt.xlabel("log(dx)")
plt.ylabel("log(error)")
plt.savefig(saved_graphs_dir + "log-scale-forward_difference.png")
plt.show()

plt.plot(np.log2(dx_range), np.log2(backward_difference_error["1st Order"]))
plt.plot(np.log2(dx_range), np.log2(backward_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(backward_difference_error["3rd Order"]))
plt.legend(["1st Order", "2nd Order", "3rd Order"])
plt.title("Backward Difference (log-log scale)")
plt.xlabel("log(dx)")
plt.ylabel("log(error)")
plt.savefig(saved_graphs_dir + "log-scale-backward_difference.png")
plt.show()

plt.plot(np.log2(dx_range), np.log2(central_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(central_difference_error["4th Order"]))
plt.legend(["2nd Order", "4th Order"])
plt.title("Central Difference (log-log scale)")
plt.xlabel("log(dx)")
plt.ylabel("log(error)")
plt.savefig(saved_graphs_dir + "log-scale-central_difference.png")
plt.show()

plt.plot(np.log2(dx_range), np.log2(forward_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(backward_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(central_difference_error["2nd Order"]))
plt.legend(["forward", "backward", "central"])
plt.title("Forward vs Backward Vs Central (2nd Order- log-log scale)")
plt.xlabel("log(dx)")
plt.ylabel("log(error)")
plt.savefig(saved_graphs_dir + "log-scale-second_order.png")
plt.show()

plt.plot(np.log2(dx_range), np.log2(forward_difference_error["1st Order"]))
plt.plot(np.log2(dx_range), np.log2(forward_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(forward_difference_error["3rd Order"]))
plt.plot(np.log2(dx_range), np.log2(backward_difference_error["1st Order"]))
plt.plot(np.log2(dx_range), np.log2(backward_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(backward_difference_error["3rd Order"]))
plt.plot(np.log2(dx_range), np.log2(central_difference_error["2nd Order"]))
plt.plot(np.log2(dx_range), np.log2(central_difference_error["4th Order"]))
plt.legend(["Forward-1st Order", "Forward-2nd Order", "Forward-3rd Order", "Backward-1st Order", 
	"Backward-1st Order", "Backward-1st Order", "Backward-1st Order", "Backward-1st Order"])
plt.title("Forward vs Central vs Backward (Log Scale)")
plt.xlabel("log(dx)")
plt.ylabel("log(error)")
plt.savefig(saved_graphs_dir + "log-scale-all.png")
plt.show()
