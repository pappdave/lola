#!/usr/bin/python

import sys
import os
import math

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
sys.path.insert(0, lib_dir)

from lola.partition_tree import PartitionTree
import lola.util


STARTING_COORD = (0.5, 0.5)

node_count = int(sys.stdin.readline())

ptree = PartitionTree((0.0, 0.0), (1.0, 1.0), depth=10)

for line in sys.stdin:
    row = line.rstrip().split()
    ptree.insert((float(row[0]), float(row[1])))

path = [ STARTING_COORD ]
current_coord = STARTING_COORD

while True:
    current_coord = ptree.get_closest_to(current_coord)

    if current_coord is None:
        break

    path.append(current_coord)
    ptree.remove(current_coord)
    
print(lola.util.get_path_length(path))
