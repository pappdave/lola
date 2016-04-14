#!/usr/bin/python

import sys
import math

def get_distance(coord1, coord2):
    """ Given two tuples representing Cartesian coordinates, return the
    Euclidean distance """

    diff_x = coord1[0] - coord2[0]
    diff_y = coord1[1] - coord2[1]
    return math.sqrt(diff_x * diff_x + diff_y * diff_y)

def get_closest_coord_index(current_coord, coords):
    """ Return the index of the coordinate in the coords list which is the
    closest to current_coord """

    min_index = 0
    min_distance = get_distance(current_coord, coords[0])
    for i in range(1, len(coords)):
        current_distance = get_distance(current_coord, coords[i])
        if current_distance < min_distance:
            min_index = i
            min_distance = current_distance

    return min_index

def get_path_length(path):
    """ Return the length of the given path """

    length = 0.0
    for i in range(1, len(path)):
        length += get_distance(path[i - 1], path[i])

    return length
    

STARTING_COORD = (0.5, 0.5)

node_count = int(sys.stdin.readline())

coords = []
for line in sys.stdin:
    row = line.rstrip().split()
    coords.append((float(row[0]), float(row[1])))

current_coord = STARTING_COORD
path = [ STARTING_COORD ]
while len(coords) > 0:
    next_coord_index = get_closest_coord_index(current_coord, coords)
    current_coord = coords[next_coord_index]
    path.append(current_coord)
    del coords[next_coord_index]
    
print(get_path_length(path))
