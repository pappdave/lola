#!/usr/bin/python

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(os.path.dirname(current_dir), 'lib')
sys.path.insert(0, lib_dir) 

from lola.partition_tree import PartitionTree

class TestPartitionTree(unittest.TestCase):
    
    def test_get_next_pivot(self):
        pivot = PartitionTree._get_next_pivot((0.0, 0.0), (1.0, 1.0))
        self.assertEqual((0.5, 0.5), pivot)

        pivot = PartitionTree._get_next_pivot((0.0, 0.25), (2.0, 0.75))
        self.assertEqual((1.0, 0.5), pivot)

        pivot = PartitionTree._get_next_pivot((1.0, 2.0), (3.0, 4.0))
        self.assertEqual((2.0, 3.0), pivot)

    def test_get_next_partitions(self):
        topleft = (0.0, 0.0)
        bottomright = (1.0, 1.0)
        pivot = PartitionTree._get_next_pivot(topleft, bottomright)
        partitions = PartitionTree._get_next_partitions(topleft, bottomright, pivot, 0)
        self.assertEqual(((0.0, 0.0), (1.0, 0.5)), partitions[0])
        self.assertEqual(((0.0, 0.5), (1.0, 1.0)), partitions[1])

        partitions = PartitionTree._get_next_partitions(topleft, bottomright, pivot, 1)
        self.assertEqual(((0.0, 0.0), (0.5, 1.0)), partitions[0])
        self.assertEqual(((0.5, 0.0), (1.0, 1.0)), partitions[1])


        topleft = (0.0, 0.0)
        bottomright = (1.0, 0.5)
        pivot = PartitionTree._get_next_pivot(topleft, bottomright)
        partitions = PartitionTree._get_next_partitions(topleft, bottomright, pivot, 0)
        self.assertEqual(((0.0, 0.0), (1.0, 0.25)), partitions[0])
        self.assertEqual(((0.0, 0.25), (1.0, 0.5)), partitions[1])

        partitions = PartitionTree._get_next_partitions(topleft, bottomright, pivot, 1)
        self.assertEqual(((0.0, 0.0), (0.5, 0.5)), partitions[0])
        self.assertEqual(((0.5, 0.0), (1.0, 0.5)), partitions[1])


        topleft = (0.123, 0.456)
        bottomright = (0.789, 0.987)
        pivot = PartitionTree._get_next_pivot(topleft, bottomright)
        partitions = PartitionTree._get_next_partitions(topleft, bottomright, pivot, 0)
        self.assertEqual(((0.123, 0.456), (0.789, 0.7215)), partitions[0])
        self.assertEqual(((0.123, 0.7215), (0.789, 0.987)), partitions[1])

        partitions = PartitionTree._get_next_partitions(topleft, bottomright, pivot, 1)
        self.assertEqual(((0.123, 0.456), (0.456, 0.987)), partitions[0])
        self.assertEqual(((0.456, 0.456), (0.789, 0.987)), partitions[1])

    def test_create_partition_tree(self):
        tree = []
        topleft = (0.0, 0.0)
        bottomright = (1.0, 1.0)
        PartitionTree._create_partition_tree(tree, topleft, bottomright, 1)
        self.assertTrue((0.5, 0.5) in tree[0])
        self.assertEqual(tree[0][(0.5, 0.5)], [[], []])

        tree = []
        PartitionTree._create_partition_tree(tree, topleft, bottomright, 2)
        self.assertTrue((0.5, 0.5) in tree[0])
        self.assertEqual(len(tree[0]), 1)
        self.assertTrue((0.5, 0.25) in tree[0][(0.5, 0.5)][0])
        self.assertEqual(tree[0][(0.5, 0.5)][0][(0.5, 0.25)], [[], []])
        self.assertTrue((0.5, 0.75) in tree[0][(0.5, 0.5)][1])
        self.assertEqual(tree[0][(0.5, 0.5)][1][(0.5, 0.75)], [[], []])

    def test_insert(self):
        ptree = PartitionTree((0.0, 0.0), (1.0, 1.0), 2)
        ptree.insert((0.1, 0.1))
        ptree.insert((0.2, 0.2))
        ptree.insert((0.6, 0.6))
        self.assertEqual([[(0.1, 0.1), (0.2, 0.2)], []], ptree.tree[0][(0.5, 0.5)][0][(0.5, 0.25)])
        self.assertEqual([[], [(0.6, 0.6)]], ptree.tree[0][(0.5, 0.5)][1][(0.5, 0.75)])

    def test_get_closest_to(self):
        ptree = PartitionTree((0.0, 0.0), (1.0, 1.0), 2)
        ptree.insert((0.1, 0.1))
        ptree.insert((0.2, 0.2))
        ptree.insert((0.6, 0.6)) 
        closest = ptree.get_closest_to((0.5, 0.5))
        self.assertEqual((0.6, 0.6), closest)

if __name__ == '__main__':
    unittest.main()

