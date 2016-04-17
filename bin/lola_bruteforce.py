#!/usr/bin/python

import math
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
sys.path.insert(0, lib_dir)

import lola.util


STARTING_COORD = (0.5, 0.5)

node_count = int(sys.stdin.readline())

coords = []
for line in sys.stdin:
    row = line.rstrip().split()
    coords.append((float(row[0]), float(row[1])))

current_coord = STARTING_COORD
path = [ STARTING_COORD ]
while coords:
    next_coord_index = lola.util.get_closest_coord_index(current_coord, coords)
    current_coord = coords[next_coord_index]
    path.append(current_coord)
    del coords[next_coord_index]
    
print(lola.util.get_path_length(path))
