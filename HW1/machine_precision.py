import numpy as np 
import argparse

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

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Data Type and Starting Value is expected')

	parser.add_argument("-p", "--precision", type = str, default = "single", help = "Data Type")
	parser.add_argument("-s", "--start_value", type = float, default = 1, help = "Starting Value of the iteration to find machine precision")

	args = parser.parse_args()

	data_type_dictionary = {
	"single" : np.float32,
	"double" : np.float64
	}

	machine_precision, num_iterations = get_machine_precision(args.start_value, data_type_dictionary[args.precision])

	print("Data Type : ", data_type_dictionary[args.precision])
	print("Machine Precision : ", machine_precision)
	print("Number of iterations required to get to the precision from start value ({}) = {}".format(args.start_value, num_iterations))
