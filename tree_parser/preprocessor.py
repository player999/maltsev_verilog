#!/usr/bin/python3
import sys
import re
import random
import copy
from configs import *


def fix_syntax(program):
	program = remove_comments(program)
	program = re.sub("[\ \t]+", " ", program)
	program = re.sub("\\( ", "(", program)
	program = re.sub(" \\)", ")", program)
	program = re.sub("^\s+", "", program)
	program = re.sub("\s+$", "", program)
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
	program = " ".join(program.split('\n'))
	program = re.sub("[\ \t]+", " ", program)
	program = re.sub("\\(\s*?", "(", program)
	program = re.sub("\s*?\\)", ")", program)
	program = rx.sub("\"\g<1>\"", program)
	program = re.sub("\\(", "[", program)
	program = re.sub("\\)", "]", program)
	program = re.sub(" ", ", ", program)
	program = eval("[" + program + "]")
	return program


def getBaseFunctions():
	baselist = open(BASIS_FUNCTIONS_FILE).read()
	baselist = baselist.splitlines()
	namelist = []
	for i in range(0, len(baselist)):
		namelist.extend([baselist[i].split("\t")[0]])
	return namelist


def getArgumentCount(body, allfnames):
	names = set(re.findall(r'[A-Za-z][A-Za-z0-9]*', body))
	arguments = names - set.intersection(allfnames, names)
	return len(arguments)


def getDefinedFunctions(tree):
	defuns = []
	for entry in tree:
		if entry[0] != "def":
			continue
		defuns.extend([{"name": entry[1], "body": entry[2], "arguments": entry[3]}])
	return defuns


def checkDefun(defuns, fname):
	for entry in defuns:
		if entry["name"] == fname:
			return entry
	return None


def getMain(tree):
	for entry in tree:
		if entry[0] == "MAIN":
			return entry[1]


def walkTree(tree, defuns):
	uber_function = checkDefun(defuns, tree[0])
	if uber_function is not None:
		if len(tree) > 1:
			tree = subArguments(tree, copy.deepcopy(uber_function), defuns)
		for i in range(0, len(tree[-1])):
			if isinstance(tree[-1][i], list):
				tree[-1][i], defuns = walkTree(tree[-1][i], defuns)
		if len(tree) == 3:
			for i in range(0, len(tree[1])):
				tree[1][i], defuns = walkTree(tree[1][i], defuns)
		tree, defuns = walkTree(tree, defuns)
	elif isinstance(tree, list):
		if len(tree) == 3:
			for i in range(0, len(tree[1])):
				tree[1][i], defuns = walkTree(tree[1][i], defuns)
		if len(tree) == 2:
			for i in range(0, len(tree[-1])):
					tree[-1][i], defuns = walkTree(tree[-1][i], defuns)
	return tree, defuns


def subArguments(tree, uber_function, defuns):
	if len(tree[-1]) != len(uber_function["arguments"]):
		raise Exception("Argument count mismatch")
	retval = [uber_function["body"][0]]
	if len(uber_function["body"]) == 3:
		retval.extend([uber_function["body"][1]])
	retval.extend([uber_function["body"][-1]])
	for i in range(0, len(uber_function["arguments"])):
		arg_name = tree[-1][i]
		arg2replace = uber_function["arguments"][i]
		for j in range(0, len(retval[-1])):
			if retval[-1][j] == arg2replace:
				retval[-1][j] = arg_name
	return retval


def subTree(tree):
	main_function = getMain(tree)
	defun = getDefinedFunctions(tree)
	tree, defun = walkTree(main_function, defun)
	return tree

def convert2primitives(text):
	tree = build_ltree(text)
	tree = subTree(tree)
	tree = makeTree(tree)
	return tree


def remove_comments(text):
	text = re.sub(r'#[^!].*', '', text)
	text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
	return text


def include_libs(text):
	res = re.findall(r'#!include (.*)', text)
	if res is None:
		return text
	for i in range(0, len(res)):
		incl = preprocess_file('./' + LIBRARY_FUNCTIONS_DIR + '/' + res[i])
		text = re.sub(r'#!include %s' % res[i], incl, text)
	return text

def preprocess_text(text):
	text = fix_syntax(text)
	text = check_syntax(text)
	text = include_libs(text)
	return text


def preprocess_file(fname):
	text = open(fname, "r").read()
	text = preprocess_text(text)

	return text


def makeTree(program):
	tree = process_node(program)
	return tree


def process_node(program):
	if isinstance(program, str):
		return program
	if isinstance(program, list):
		if len(program) == 1:
			if isinstance(program[0], str):
				node = {"name": program[0], "static": "", "arguments": "",
						"id": str(int(99999 + random.random() * 900000))}
				return node
	node = {"name": program[0], "arguments": [], "static": []}
	if len(program) == 3:
		for i in range(0, len(program[1])):
			node["static"].extend([process_node(program[1][i])])
	node["id"] = str(int(99999 + random.random() * 900000))
	for i in range(0, len(program[-1])):
		arg = {"no": i, "value": process_node(program[-1][i])}
		node["arguments"].extend([arg])
	return node


if __name__ == '__main__':
	if len(sys.argv) != 2:
		quit()
	text = preprocess_file(sys.argv[1])
	text = convert2primitives(text)