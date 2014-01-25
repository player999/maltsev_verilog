#!/usr/bin/env python
import re
import random

def parseParentheses(string):
	retval = []
	random.seed()
#Check validity
	if len(re.findall("\(", string)) != len(re.findall("\)", string)):
		return retval
#Preprocess
	for i in range(0,len(string)-2):
		if string[i] == ' ':
			string = string[:i] + string[i+1:] 
#Parose
	retval = parseExp(string)
	return retval

def parseExp(string):
	arguments = re.search('\(.*\)', string)
	arguments = arguments.group(0)
	arguments = arguments[1:-1]
	function_name = re.search('.*?\(', string)
	function_name = function_name.group(0)
	function_name = function_name[0:-1]
	splitted_arguments = []
	static_arguments = []
	depth = 0
	line = ""
	for i in arguments:
		if i == '(':
			depth = depth + 1
		if i == ')':
			depth = depth - 1
		line = line + i
		if depth == 0:
			if i == ';' or i == ',':
				splitted_arguments.extend([line[:-1]])
				if i == ';':
					static_arguments = splitted_arguments
					splitted_arguments = []
				line = ""
	splitted_arguments.extend([line])
	root = {}
	root["name"] = function_name
	root["id"] = str(int(99999 + random.random() * 900000))
	root["arguments"] = splitted_arguments
	root["static"] = static_arguments
	for i in range(0, len(root["arguments"])):
		arg = root["arguments"][i]
		root["arguments"][i] = {}
		if len(re.findall("\(", arg)) > 0:
			root["arguments"][i]["value"] = parseExp(arg)
			if isinstance(root["arguments"][i]["value"], dict):
				root["arguments"][i]["no"] = i;
		else:
			root["arguments"][i]["value"] = arg;
			root["arguments"][i]["no"] = i;

	return root
if __name__ == '__main__':
	teststring1 = "I(2,3;X,add(s(x), m(g(n), 5)),Z)"
	teststring2 = "add(mul(X,Y),Z)"
	teststring3 = "R(i(0;x,y),i(0;s(x),y,z);x,y)"
	res = parseParentheses(teststring3)
	print(res)
