# Check README.md for instruction to run

import numpy as np 
import argparse
import sys

#####################################################
# Function to calculate the machine precision/epsilon
# start_value - value from where we will start the iteration, 
# i.e., we will keep on halving the start_value until 1+start_value == 1
# data_type - data type for which we need to find the machine precision.
#####################################################
def get_machine_precision(start_value = 1, data_type = np.float16):

	num_iterations = 0
	machine_precision = data_type(start_value)
	while True:
		num_iterations += 1
		if data_type(1+machine_precision/2) != data_type(1):
			machine_precision = data_type(machine_precision/2)
		else: 
			break

	return machine_precision, num_iterations


###############################################
# I have created a parser to accept command line argument
# This code can accept two command line arguments - 
# 1. precision: can be single (32 bit float) or double (64 bit float)
# 2. start_value: starting value of the algorithm used to find the machine precision

# If no command line argument is passed, default value of precision is single (32 bit float)
# and defalut value of start_value is 1.
################################################
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Data Type and Starting Value is expected')

	parser.add_argument("-p", "--precision", type = str, default = "single", help = "Data Type")
	parser.add_argument("-s", "--start_value", type = float, default = 1, help = "Starting Value of the iteration to find machine precision")

	args = parser.parse_args()

	if args.precision != "single" and args.precision != "double":
		print("Invalid Precision")
		sys.exit()

	# Dictionary to map precision to the corresponding data type.
	data_type_dictionary = {
	"single" : np.float32,
	"double" : np.float64
	}

	machine_precision, num_iterations = get_machine_precision(args.start_value, data_type_dictionary[args.precision])

	print("Data Type : ", data_type_dictionary[args.precision])
	print("Machine Precision : ", machine_precision)
	print("Number of iterations required to get to the precision from start value ({}) = {}".format(args.start_value, num_iterations))
