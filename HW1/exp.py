import numpy as np 

def exp(x = 10):

	num_terms = 0
	sum_terms = 0
	i = 1
	term = 1
	while (term != float("inf") and term != float("nan")):
		# print(term)
		# if term == 0:
		# 	break
		sum_terms += term
		term *= x/i
		num_terms += 1
		i += 1

	return sum_terms, num_terms

print(exp(-5)[0], np.exp(-5))
print(exp(-10)[0], np.exp(-10))
print(exp(-50)[0], np.exp(-50))