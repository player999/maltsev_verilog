#!/usr/bin/python3
#-*-tab-width:4-*-

import re
import random

def fix_syntax(program):
	program = re.sub("//.*","", program)
	program = re.sub("\s+", " ", program)
	program = re.sub("\\( ","(", program)
	program = re.sub(" \\)",")", program)
	program = re.sub("^\s+","", program)
	program = re.sub("\s+$","", program)
	return program

def check_syntax(program):
	left_pc = len(re.findall("\\(", program))
	right_pc = len(re.findall("\\)", program))
	if left_pc != right_pc:
		print("Error: Parentheses parity violation!")
		return None
	return program

def build_ltree(program):
	rx = re.compile(r'([a-zA-Z0-9]+)')
	program = rx.sub("\"\g<1>\"", program)
	program = re.sub("\\(","[", program)
	program = re.sub("\\)","]", program)
	program = re.sub(" ",", ", program)
	print(program)
	program = eval(program) 
	return program

def walk_program(program):
	if program == None:
		return rogram
	if isinstance(program, list):
		program = check_listsyntax(program)
		if program == None:
			return program
		root = {}
		root["name"] = program[0]
		root["id"] = str(int(99999 + random.random() * 900000))
		if len(program) == 2:
			arguments = program[1]
			static  = []
		elif len(program) == 3:
			arguments = program[2]
			static = program[1]
		root["arguments"] = []
		root["static"] = []
		for i in range(0, len(arguments)):
			root["arguments"].extend([{}])
			root["arguments"][i]["no"] = i
			root["arguments"][i]["value"] = walk_program(arguments[i])
		for i in range(0, len(static)):
			root["static"].extend([{}])
			root["static"][i] = walk_program(static[i])
		return root
	if isinstance(program, str):
		return program
	if isinstance(program, int):
		return str(program)
	print("Something wrong")
		

def check_listsyntax(program):
	if len(program) < 2:
		print("List is too short")
		print(program)
		return None
	if not isinstance(program[0], str):
		print("Function name can not be a list")
		print(program[0])
		return None
	if len(program) == 3:
		if not isinstance(program[1], list):
			print("Static arguments must be a list")
			print(program[1])
			return None
		if not isinstance(program[2], list):
			print("Dynamic arguments must be a list")
			print(program[2])
			return None
	if len(program) == 2:
		if not isinstance(program[1], list):
			print("Dynamic arguments must be a list")
			print(program[2])
			return None
	if len(program) > 3:
		print("Too many arguments!")
		return None
	return program

def parse_program(program):
	program = fix_syntax(program)
	program = check_syntax(program)
	if program == None:
		return
	program = build_ltree(program)
	program = walk_program(program)
	return program

if __name__=="__main__":
	example = """
(mul (
	(add (D E))
	(R (A (add (A B))) 	 (A B  	C))
	))

"""
	example1 = """
(R (
		(i ( 0 ) (x y))
		y
		z
   )
   (x y)
)	
"""
#	R(i(0;x,y),i(0;s(x),y,z);x,y)
	print(parse_program(example1))
