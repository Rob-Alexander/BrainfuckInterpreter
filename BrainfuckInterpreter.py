#!/usr/bin/env python3

import sys

VERBOSE = True

def interprete(src, inp = None):
	## STUB ## - Throw syntax error if filter finds any non-allowed characters (except whitespace) 
	src = sanitize(src)

	instr = 0
	count = 1
	ptr = 0
	mem = [0] * 30000
	jmp = loadJmps(src)
	out = ""


	while instr < len(src):
		cmd = str(src[instr])

		if VERBOSE: print(
			"Count: {:4d} | Instr: {:3d} | Cmd: {:1s} | Ptr: {:3d} | Val: {:3d}({:1s}) | Result: "
			.format(count, instr, cmd, ptr, mem[ptr], chrp(mem[ptr])),
			end = '', flush = True
			)

		if cmd == '<':
			ptr = ptr - 1 if ptr > 0 else 29999
			if VERBOSE: print("ptr=" + str(ptr))


		if cmd == '>':
			ptr = ptr + 1 if ptr < 29999 else 0
			if VERBOSE: print("ptr=" + str(ptr))


		if cmd == '+':
			mem[ptr] = mem[ptr] + 1 if mem[ptr] < 255 else 0
			if VERBOSE: print("val=" + str(mem[ptr]) + "(" + chrp(mem[ptr]) + ")")


		if cmd == '-':
			mem[ptr] = mem[ptr] - 1 if mem[ptr] > 0 else 255
			if VERBOSE: print("val=" + str(mem[ptr]) + "(" + chrp(mem[ptr]) + ")")


		if cmd == '.':
			out += chr(mem[ptr])
			if VERBOSE: print("output=" + out)


		if cmd == ',':
			mem[ptr] = ord(inp)
			if VERBOSE: print("input=" + ord(inp) + "(" + chrp(inp) + ")")


		if cmd == '[':
			if mem[ptr] == 0:
				instr = jmp[instr]
				if VERBOSE: print("jmp=" + str(instr))
			else:
				if VERBOSE: print("nojmp;val!=0")


		if cmd == ']':
			if mem[ptr] != 0:
				instr = jmp[instr]
				if VERBOSE: print("jmp=" + str(instr))
			else:
				if VERBOSE: print("nojmp;val==0")


		instr += 1
		count += 1

	return out

def loadJmps(src):
	stack = []
	jmp = {}

	for pos, cmd in enumerate(src):
		if cmd == '[':
			stack.append(pos)
		if cmd == ']':
			if len(stack) == 0:
				print("Syntax Error: End brackets must have matching start brackets.")
				quit()
			start = stack.pop()
			jmp[start] = pos
			jmp[pos] = start

	if len(stack) > 0:
		print("Syntax Error: Start brackets must have matching end brackets.")
		quit()

	return jmp


def sanitize(src):
	return list(filter(lambda x: x in ['<', '>', '+', '-', '.', ',', '[', ']'], src))

def chrp(chrOrd):
	if chrOrd < 32:
		chrOrd = ord(' ')
	return chr(chrOrd)

def main():
	if len(sys.argv) == 3: 
		print(interprete(str(sys.argv[1]), str(sys.argv[2])))
	elif len(sys.argv) == 2: 
		print(interprete(str(sys.argv[1])))
	else: 
		print("Usage:", sys.argv[0], "src inp")

if __name__ == "__main__": main()
