# CFD Assignment 1

Instructions for running the python scripts are as follows: 

## Machine Precision

The script machine_precision.py accepts two command line arguments.

`python machine_precision.py -p single -s 0.5`

or

`python machine_precision.py --precision double --start_value 0.25`

If no command line arguments are passed, then the program used the default values of precision (single) and start_value (1).

precision accepts either single or double as argument whereas start_value accepts any floating point number.

## exp(x)

The script exp.py accepts one command line argument.

`python exp.py -x 14`

x is the value whose exp is to be evaluated. If no argument is passed, then the code used default value of x as -5.

## Matrix multiplication

The script matrix_multiplication.py takes one command line argument. 

`python matrix_multiplication.py input_array.txt`

Here, input_array.txt is a file where one can give the 2 matrices to be multiplied as input. 
A sample matrix input file is attached as a reference for the input format.

## Finite Difference

`python finite_differences.py` 

This script does not take any command line argument. It creates a directory named Graphs-Finite_Differences in which it stores the various error vs dx graphs.

