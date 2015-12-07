import numpy as np
import re

with open('input.txt', 'r') as f: input = f.read().splitlines()
lights = np.zeros(shape=(1000,1000), dtype=np.int64)
expression = re.compile('([a-zA-Z ]+) (\d+),(\d+) through (\d+),(\d+)')

def parse_instruction(s):
    m = expression.match(s)
    (operation, x1, y1, x2, y2) = m.groups()
    x1, x2, y1, y2 = int(x1), int(x2)+1, int(y1), int(y2)+1
    return (operation, x1, x2, y1, y2)

for instruction in input:
    (operation, x1, x2, y1, y2) = parse_instruction(instruction)
    if operation == 'toggle':
        lights[x1:x2,y1:y2] += 2

    elif operation == 'turn on':
        lights[x1:x2,y1:y2] += 1

    elif operation == 'turn off':
        lights[x1:x2,y1:y2] -= 1
        lights[lights < 0] = 0  # stop at 0'

print lights.sum()

# 14110788