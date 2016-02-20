#!/usr/bin/python
## Script to convert roman numericals in English
#Author: Hitesh Agrawal , hitesha1981@gmail.com
val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
a = 0
my_keys = val.keys()

while a == 0:
	input = str(raw_input("Enter a roman number: "))
	for alpha in input:
		if alpha.upper() in my_keys:
			a = 2
		else:
			a = 0
			print "Enter a proper roman number: "
			break	 

total = 0
input = input.upper()
while input:
	if len(input) == 1 or val[input[0]] >= val[input[1]]:
		total += val[input[0]]
		input = input[1:]
	else:
		total += val[input[1]] - val[input[0]]
		input = input[2:]

print "The numeric value is" , total		
							