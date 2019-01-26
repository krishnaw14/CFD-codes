# Check README.md for instruction to run

import numpy as np 
import argparse

'''
Function to calculate exp(x) for the given x passed as an argument
Taylor Series expansion of exp(x) is such that: 
T_i = x^i/i! where i = 0, 1, 2, 3 ...
So, T_i/T_{i-1} = x/i 

So, the algorithm for evaluation exp(x) starts with the first term 1 and subsequently finds each term by multiplying by x/i.
All theses terms are summed and the loop continues until the subsequent term becomes NaN, inf or zero.

I also find the number of terms that were summed to get the function value.
'''
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


'''
A parser is created to accept command line argument
This code can accept one command line arguments - 
1. x: Value whose exp(x) is required to be calculated

If no command line argumennt is passed, default value of x is -5.
'''
if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='x for which exp(x) is to be computed')
	parser.add_argument("-x", type = float, default = -5, help='x for which exp(x) is to be computed')
	args = parser.parse_args()

	answer, num_terms = exp(args.x)
	exact_value = np.exp(args.x) # Exact Answer is found using the in-built function in numpy
	error = 100*abs(answer - exact_value)/exact_value # Error is evaluated in percentage by comparing with the exact_value

	print("x = ", args.x)
	print("Obtained Value: ", answer) 
	print("Exact Value:", exact_value)
	print("Error (%) : ", error )
	print("Number of terms: ", num_terms, "\n")
