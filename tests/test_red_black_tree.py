from red_black_tree.red_black_tree import RedBlackTree
import unittest
import random
import timeit


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

    def test_random_add_then_remove(self):
        # Given
        TEST_SIZE = 10000
        TEST_RANGE = 100000
        test_rbt = RedBlackTree()
        test_input = random.sample(range(-TEST_RANGE, TEST_RANGE), TEST_SIZE)
        total_time_spent = 0

        # When
        min_key = TEST_RANGE
        for test_key in test_input:
            min_key = min(min_key, test_key)
            total_time_spent += timeit.timeit(
                lambda: test_rbt.add(test_key, test_key), number=1)
            self.assertEqual(min_key, test_rbt.first()[0])

        # Then
        test_output = sorted(test_input)
        for test_key in test_output:
            total_time_spent += timeit.timeit(
                lambda: self.assertEqual(test_key, test_rbt.pop()[0]), number=1)
        print(f'Total running time for {TEST_SIZE} keys: {total_time_spent}')

    def test_random_mixed_add_remove(self):
        # Given
        test_rbt = RedBlackTree()
        TEST_SIZE = 10000
        TEST_RANGE = 100000
        test_input = random.sample(range(-TEST_RANGE, TEST_RANGE), TEST_SIZE)
        total_time_spent = 0

        # When & Then - add only
        min_key = TEST_RANGE
        for test_key in test_input[:TEST_SIZE // 2]:
            min_key = min(min_key, test_key)
            total_time_spent += timeit.timeit(
                lambda: test_rbt.add(test_key, test_key), number=1)
            self.assertEqual(min_key, test_rbt.first()[0])

        # When & Then - add then remove
        existing_keys = test_input[:TEST_SIZE // 2]
        for test_key in test_input[TEST_SIZE // 2:]:
            existing_keys.append(test_key)
            total_time_spent += timeit.timeit(
                lambda: test_rbt.add(test_key, test_key), number=1)
            rm_key = random.sample(existing_keys, 1)[0]
            total_time_spent += timeit.timeit(
                lambda: test_rbt.remove(rm_key), number=1)
            existing_keys.remove(rm_key)
            total_time_spent += timeit.timeit(
                lambda: self.assertEqual(
                    min(existing_keys), test_rbt.first()[0]), number=1)

        # When & Then - remove only
        test_output = sorted(existing_keys)
        for test_key in test_output:
            total_time_spent += timeit.timeit(
                lambda: self.assertEqual(test_key, test_rbt.pop()[0]), number=1)
        print(f'Total running time for {TEST_SIZE} keys: {total_time_spent}')


if __name__ == '__main__':
    unittest.main()
