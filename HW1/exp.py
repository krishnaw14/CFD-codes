import numpy as np 
import argparse

def exp(x = 10):

	num_terms = 0
	sum_terms = 0
	i = 1
	term = 1
	while (term != float("inf") and term != float("nan") and term != 0):
		sum_terms += term
		term *= x/i
		num_terms += 1
		i += 1

	return sum_terms, num_terms


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='x for which exp(x) is to be computed')
	parser.add_argument("-x", type = float, default = -5, help='x for which exp(x) is to be computed')
	args = parser.parse_args()

	answer, num_terms = exp(args.x)
	exact_value = np.exp(args.x)
	error = 100*abs(answer - exact_value)/exact_value

	print("x = ", args.x)
	print("Obtained Value: ", answer) 
	print("Exact Value:", exact_value)
	print("Error (%) : ", error )
	print("Number of terms: ", num_terms, "\n")
