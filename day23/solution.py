import re

# --- Day 23: Opening the Turing Lock ---

# Little Jane Marie just got her very first computer for Christmas from some unknown benefactor.
# It comes with instructions and an example program, but the computer itself seems to be malfunctioning.
# She's curious what the program does, and would like you to help her run it.

# The manual explains that the computer supports
# two registers and
# six instructions
# (truly, it goes on to remind the reader, a state-of-the-art technology).

class Computer(object):
	def __init__(self, a=0, b=0):
		super(Computer, self).__init__()
		# The registers are named a and b, can hold any non-negative integer, and begin with a value of 0.
		self.registers = {'a': a, 'b': b}
		self.eip = 0 # pointer to the next instruction

	# The instructions are as follows:

	def hlf(self, r, *_):
		# hlf r sets register r to half its current value, then continues with the next instruction.
		self.registers[r] //= 2
		self.eip += 1

	def tpl(self, r, *_):
		# tpl r sets register r to triple its current value, then continues with the next instruction.
		self.registers[r] *= 3
		self.eip += 1
	
	def inc(self, r, *_):
		# inc r increments register r, adding 1 to it, then continues with the next instruction.
		self.registers[r] += 1
		self.eip += 1
	
	def jmp(self, _, offset):
		# jmp offset is a jump; it continues with the instruction offset away relative to itself.
		self.eip += offset
		# self.eip = (self.eip + offset) % len(instructions)
	
	def jie(self, r, offset):
		# jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
		if self.registers[r] % 2 == 0:
			self.eip += offset
			# self.eip = (self.eip + offset) % len(instructions)
		else:
			self.eip += 1

	def jio(self, r, offset):
		# jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
		if self.registers[r] == 1:
			self.eip += offset
			# self.eip = (self.eip + offset) % len(instructions)
		else:
			self.eip += 1

	def compute(self, instructions, stop_at=1000000):
		self.instructions = dict(enumerate(instructions))
		self.eip = 0
		operations = 0

		instruction_template = re.compile(r"(hlf|tpl|inc|jmp|jie|jio) (a|b)?,? ?(.*)")
		try:
			while operations < stop_at:
				instruction, register, offset = instruction_template.match(self.instructions[self.eip]).groups()
				# print 'EIP=%s - running %s(%s, %s)' % (self.eip, instruction, register, offset)
				getattr(self, instruction)(register, offset and int(offset))
				operations += 1
				# print 'state - a: %s, b: %s' % tuple(self.registers.values())
		except Exception, e:
			print '\n\nerror: %s' % e
			print 'EIP: %s' % self.eip
			print 'a: %s; b: %s\n\n' % tuple(self.registers.values())

			
# All three jump instructions work with an offset relative to that instruction.
# The offset is always written with a prefix + or - to indicate the direction of the jump
# (forward or backward, respectively). For example, jmp +1 would simply continue with the next instruction,
# while jmp +0 would continuously jump back to itself forever.

# The program exits when it tries to run an instruction beyond the ones defined.

# For example, this program sets a to 2, because the jio instruction causes it to skip the tpl instruction:

instructions = """
inc a
jio a, +2
tpl a
inc a
""".splitlines()[1:]

c = Computer()
c.compute(instructions)
assert c.registers['a'] == 2

# What is the value in register b when the program in your puzzle input is finished executing?

with open('input.txt', 'r') as f: input = f.read().splitlines()
machine_1 = Computer()
machine_1.compute(input, stop_at=2000)


# --- Part Two ---

# The unknown benefactor is very thankful for releasi-- er, helping little Jane Marie with her computer.
# Definitely not to distract you, what is the value in register b after the program is finished executing
# if register a starts as 1 instead?

machine_2 = Computer(a=1)
machine_2.compute(input, stop_at=2000)