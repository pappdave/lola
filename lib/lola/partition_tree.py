
import math

class PartitionTree:
    """ A class representing a tree used for partitioning a 2d space """

    @staticmethod
    def _get_next_pivot(topleft, bottomright):
        """ Return the next pivot used for partitioning """

        return ((topleft[0] + bottomright[0]) / 2, (topleft[1] + bottomright[1]) / 2)

    @staticmethod
    def _get_next_partitions(topleft, bottomright, pivot, axis):
        """ Create a list of new partitions """

        if axis == 0:
            return [(topleft, (bottomright[0], pivot[1])), ((topleft[0], pivot[1]), bottomright)]
        else:
            return [(topleft, (pivot[0], bottomright[1])), ((pivot[0], topleft[1]), bottomright)]

    @staticmethod
    def _create_partition_tree(tree, topleft, bottomright, depth):
        """ Create a partition tree with the specified depth """

        if depth <= 0:
            tree.append([])
            return

        pivot = PartitionTree._get_next_pivot(topleft, bottomright)
        axis = PartitionTree._get_axis(depth)

        partitions = PartitionTree._get_next_partitions(topleft, bottomright, pivot, axis)

        children = []
        for partition in partitions:
            PartitionTree._create_partition_tree(children, partition[0], partition[1], depth - 1)

        tree.append({pivot: children})

    @staticmethod
    def _get_axis(depth):
        return depth % 2

    def __init__(self, topleft, bottomright, depth=10):
        self.tree = []
        self.topleft = topleft
        self.bottomright = bottomright
        self.depth = depth

        self._create_partition_tree(self.tree, topleft, bottomright, depth)

    @staticmethod
    def _insert(tree, element, depth):
        if depth <= 0:
            tree.append(element)
        else:
            index = 1 - PartitionTree._get_axis(depth)
            current_pivot = tree.keys()[0]
            if element[index] <= current_pivot[index]:
                subtree = tree[current_pivot][0]
            else:
                subtree = tree[current_pivot][1]

            PartitionTree._insert(subtree, element, depth - 1)


    def insert(self, element):
        self._insert(self.tree[0], element, self.depth)

    @staticmethod
    def _get_distance(coord1, coord2):
        """ Given two tuples representing Cartesian coordinates, return the
        Euclidean distance """

        diff_x = coord1[0] - coord2[0]
        diff_y = coord1[1] - coord2[1]
        return math.sqrt(diff_x * diff_x + diff_y * diff_y)

    @staticmethod
    def _get_closest_coord_index(current_coord, coords):
        """ Return the index of the coordinate in the coords list which is the
        closest to current_coord """

        min_index = 0
        min_distance = PartitionTree._get_distance(current_coord, coords[0])
        for i in range(1, len(coords)):
            current_distance = PartitionTree._get_distance(current_coord, coords[i])
            if current_distance < min_distance:
                min_index = i
                min_distance = current_distance

        return coords[min_index]

    @staticmethod
    def _get_closest_to(tree, element, depth):
        if depth <= 0:
            if len(tree) > 0:
                return PartitionTree._get_closest_coord_index(element, tree)
            else:
                return None

        else:
            index = 1 - PartitionTree._get_axis(depth)
            current_pivot = tree.keys()[0]
            if element[index] <= current_pivot[index]:
                subtree = tree[current_pivot][0]
                other_subtree = tree[current_pivot][1]
            else:
                subtree = tree[current_pivot][1]
                other_subtree = tree[current_pivot][0]

            closest = PartitionTree._get_closest_to(subtree, element, depth - 1)
            if closest is not None:
                closest_distance = PartitionTree._get_distance(element, closest)
            if closest is None or closest_distance > abs(current_pivot[index] - element[index]):
                closest2 = PartitionTree._get_closest_to(other_subtree, element, depth - 1)
                if closest is None:
                    closest = closest2
                elif closest2 is not None:
                    closest2_distance = PartitionTree._get_distance(element, closest2)
                    if closest2_distance < closest_distance:
                        closest = closest2

            return closest
 
    def get_closest_to(self, element):
        return self._get_closest_to(self.tree[0], element, self.depth)

    @staticmethod
    def _remove(tree, element, depth):
        if depth <= 0:
            tree.remove(element)
        else:
            index = 1 - PartitionTree._get_axis(depth)
            current_pivot = tree.keys()[0]
            if element[index] <= current_pivot[index]:
                subtree = tree[current_pivot][0]
            else:
                subtree = tree[current_pivot][1]

            PartitionTree._remove(subtree, element, depth - 1)

    def remove(self, element):
        return self._remove(self.tree[0], element, self.depth)

