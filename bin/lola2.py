#!/usr/bin/python

import sys
import os
import math

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
sys.path.insert(0, lib_dir)

from lola.partition_tree import PartitionTree


def get_distance(coord1, coord2):
    """ Given two tuples representing Cartesian coordinates, return the
    Euclidean distance """

    diff_x = coord1[0] - coord2[0]
    diff_y = coord1[1] - coord2[1]
    return math.sqrt(diff_x * diff_x + diff_y * diff_y)


def get_path_length(path):
    """ Return the length of the given path """

    length = 0.0
    for i in range(1, len(path)):
        length += get_distance(path[i - 1], path[i])

    return length


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
    
print(get_path_length(path))
