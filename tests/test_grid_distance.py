import unittest
from gridable import Grid


class TestNode(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()

    def test_distance_one_dimension(self):
        grid = Grid()
        distance = grid[0].distance(grid[5])

        self.assertEqual(distance, 5)

    def test_distance_two_dimension(self):
        grid = Grid()
        distance = grid[0][0].distance(grid[5][5])

        self.assertEqual(distance, 10)

    def test_distance_three_dimension(self):
        grid = Grid()
        distance = grid[0][0][0].distance(grid[5][5][5])

        self.assertEqual(distance, 15)

    def test_distance_mismatch_dimension_fail(self):
        grid = Grid()

        exception = False
        try:
            grid[0][0][0].distance(grid[5][5])
        except:
            exception = True
        self.assertTrue(exception)
