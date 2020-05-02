from red_black_tree.red_black_tree import RedBlackTree
import unittest
import random


class TestRedBlackTree(unittest.TestCase):
    def test_init(self):
        RedBlackTree()

    def test_add(self):

        # Given
        test_rbt = RedBlackTree()

        # When & Then
        test_rbt.add(10, 100)
        test_rbt.add(5, 'test')
        test_rbt.add(15, 200)
        test_rbt.add(-1, 'string')

    def test_get_first_node(self):

        # Given
        test_rbt = RedBlackTree()
        test_rbt.add(10, 100)
        test_rbt.add(5, 'test')
        test_rbt.add(15, 200)
        test_rbt.add(-1, 'string')

        # When & Then
        self.assertEqual(test_rbt.first(), (-1, 'string'))

    def test_pop(self):

        # Given
        test_rbt = RedBlackTree()
        test_rbt.add(10, 100)
        test_rbt.add(5, 'test')
        test_rbt.add(15, 200)
        test_rbt.add(-1, 'string')

        # When & Then
        self.assertEqual(test_rbt.first(), (-1, 'string'))
        self.assertEqual(test_rbt.pop(), (-1, 'string'))
        self.assertEqual(test_rbt.first(), (5, 'test'))
        self.assertEqual(test_rbt.pop(), (5, 'test'))
        self.assertEqual(test_rbt.first(), (10, 100))
        self.assertEqual(test_rbt.pop(), (10, 100))
        self.assertEqual(test_rbt.first(), (15, 200))
        self.assertEqual(test_rbt.pop(), (15, 200))
        self.assertEqual(test_rbt.first(), None)
        self.assertEqual(test_rbt.pop(), None)

    def test_remove(self):

        # Given
        test_rbt = RedBlackTree()
        test_rbt.add(10, 100)
        test_rbt.add(5, 'test')
        test_rbt.add(15, 200)
        test_rbt.add(-1, 'string')

        # When
        test_rbt.remove(-1)
        test_rbt.remove(10)

        # Then
        self.assertEqual(test_rbt.first(), (5, 'test'))
        self.assertEqual(test_rbt.pop(), (5, 'test'))
        self.assertEqual(test_rbt.first(), (15, 200))
        self.assertEqual(test_rbt.pop(), (15, 200))

    def test_random_input(self):
        # Given
        test_rbt = RedBlackTree()
        test_input = random.sample(range(-100000, 100000), 5000)

        # When
        min_key = 100000
        for test_key in test_input:
            min_key = min(min_key, test_key)
            test_rbt.add(test_key, test_key)
            self.assertEqual(min_key, test_rbt.first()[0])

        # Then
        test_output = sorted(test_input)
        for test_key in test_output:
            self.assertEqual(test_key, test_rbt.pop()[0])


if __name__ == '__main__':
    unittest.main()
