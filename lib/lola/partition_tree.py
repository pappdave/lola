
import math
import lola.util

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
        """ Return the axis used for partitioning at the given depth """

        return depth % 2

    def __init__(self, topleft, bottomright, depth=10):
        self.tree = []
        self.topleft = topleft
        self.bottomright = bottomright
        self.depth = depth

        self._create_partition_tree(self.tree, topleft, bottomright, depth)

    @staticmethod
    def _get_subtree_index(tree, element, depth):
        index = 1 - PartitionTree._get_axis(depth)
        current_pivot = tree.keys()[0]
        if element[index] <= current_pivot[index]:
            return 0
        else:
            return 1

    @staticmethod
    def _insert(tree, element, depth):
        """ Insert element into the given tree assuming the specified depth """

        if depth <= 0:
            tree.append(element)
        else:
            index = PartitionTree._get_subtree_index(tree, element, depth)
            current_pivot = tree.keys()[0]
            subtree = tree[current_pivot][index]
            PartitionTree._insert(subtree, element, depth - 1)


    def insert(self, element):
        """ Insert the given element to the partition tree """

        self._insert(self.tree[0], element, self.depth)

    @staticmethod
    def _get_closest_to(tree, element, depth):
        """ Return the value in the given tree (assuming the specified depth)
        which is closest the element """

        if depth <= 0:
            if len(tree) > 0:
                index = lola.util.get_closest_coord_index(element, tree)
                return tree[index]
            else:
                return None

        else:
            index = PartitionTree._get_subtree_index(tree, element, depth)
            current_pivot = tree.keys()[0]
            subtree = tree[current_pivot][index]
            other_subtree = tree[current_pivot][1 - index]

            closest = PartitionTree._get_closest_to(subtree, element, depth - 1)
            if closest is not None:
                closest_distance = lola.util.get_distance(element, closest)
            if closest is None or closest_distance > abs(current_pivot[index] - element[index]):
                closest2 = PartitionTree._get_closest_to(other_subtree, element, depth - 1)
                if closest is None:
                    closest = closest2
                elif closest2 is not None:
                    closest2_distance = lola.util.get_distance(element, closest2)
                    if closest2_distance < closest_distance:
                        closest = closest2

            return closest
 
    def get_closest_to(self, element):
        """ Return the value in the tree which is closest to element """

        return self._get_closest_to(self.tree[0], element, self.depth)

    @staticmethod
    def _remove(tree, element, depth):
        """ Remove element from the given tree assuming the specified depth """

        if depth <= 0:
            tree.remove(element)
        else:
            index = PartitionTree._get_subtree_index(tree, element, depth)
            current_pivot = tree.keys()[0]
            subtree = tree[current_pivot][index]
            PartitionTree._remove(subtree, element, depth - 1)

    def remove(self, element):
        """ Remove element from the partition tree """

        return self._remove(self.tree[0], element, self.depth)

