import unittest
from gridable import Grid


class TestCell(unittest.TestCase):
    def test_equals_true(self):
        grid = Grid()
        grid[-10] = 5
        grid[10] = 5

        self.assertEqual(grid[-10], grid[10])

    def test_equals_cell_value(self):
        grid = Grid()
        grid[-10] = 5
        grid[10] = 6

        self.assertNotEqual(grid[-10], grid[10])

    def test_equals_type(self):
        grid = Grid()
        grid[-10] = 5

        self.assertEqual(grid[-10], 5)

    def test_delete(self):
        grid = Grid()
        grid[10] = 5

        del grid[10]

        self.assertEqual(grid[10].value(), None)

    def test_coordinates(self):
        grid = Grid()

        self.assertEqual(grid[10].coordinates(), (10,))
        self.assertEqual(grid[10][5].coordinates(), (10, 5))
        self.assertEqual(grid[10][5][1].coordinates(), (10, 5, 1))

    def test_one_dimension(self):
        grid = Grid()
        grid[-10] = 5
        grid[0] = 6
        grid[10] = 7

        self.assertEqual(grid[-10].value(), 5)
        self.assertEqual(grid[0].value(), 6)
        self.assertEqual(grid[10].value(), 7)

    def test_update(self):
        grid = Grid()
        grid[10] = 7
        grid[10] = 8

        self.assertEqual(grid[10].value(), 8)

    def test_iterate(self):
        grid = Grid()
        grid[-10] = 5
        grid[0] = 6
        grid[10] = 7

        values = list(grid)

        self.assertEqual(len(values), 3)

        self.assertEqual(values[0].value(), 5)
        self.assertEqual(values[0].coordinates(), (-10,))

        self.assertEqual(values[1].value(), 6)
        self.assertEqual(values[1].coordinates(), (0,))

        self.assertEqual(values[2].value(), 7)
        self.assertEqual(values[2].coordinates(), (10,))

    def test_len(self):
        grid = Grid()
        grid[-10] = 5
        grid[0] = 6
        grid[10] = 7

        self.assertEqual(len(grid), 3)

    def test_contains_index(self):
        grid = Grid()
        grid[5][0] = 5

        self.assertTrue(5 in grid)
        self.assertFalse(5 in grid[5][0])

    def test_not_contains_index(self):
        grid = Grid()
        grid[5][0] = 5

        self.assertFalse(8 in grid)

    def test_str(self):
        grid = Grid()
        grid[1][2] = 3
        grid[2][2] = 4
        grid[3][1] = 5
        grid[3][2] = 6

        self.assertEqual(str(grid), "[[3],[4],[5,6]]")
        self.assertEqual(str(grid[1]), "[3]")
        self.assertEqual(str(grid[1][2]), "3")
        self.assertEqual(str(grid[3]), "[5,6]")

    def test_contains_value(self):
        grid = Grid()
        grid[-10] = 5
        grid[0] = 6
        grid[10] = 7

        self.assertTrue(5 in grid)
        self.assertTrue(6 in grid)
        self.assertTrue(7 in grid)

    def test_not_contains_value(self):
        grid = Grid()
        grid[-10] = 5

        self.assertFalse(8 in grid)

    def test_not_subscriptable(self):
        grid = Grid()
        grid[10] = 5

        exception = False
        try:
            grid[10][1]
        except:
            exception = True

        self.assertTrue(exception)

    def test_two_dimensions(self):
        grid = Grid()
        grid[-10][-10] = 5
        grid[0][0] = 6
        grid[10][10] = 7

        self.assertEqual(grid[-10][-10].value(), 5)
        self.assertEqual(grid[0][0].value(), 6)
        self.assertEqual(grid[10][10].value(), 7)

    def test_three_dimensions(self):
        grid = Grid()
        grid[-10][-10][-10] = 5
        grid[0][0][0] = 6
        grid[10][10][10] = 7

        self.assertEqual(grid[-10][-10][-10].value(), 5)
        self.assertEqual(grid[0][0][0].value(), 6)
        self.assertEqual(grid[10][10][10].value(), 7)

    def test_set_array(self):
        grid = Grid()
        grid[0] = [10, 20, 30]

        self.assertEqual(grid[0][0].value(), 10)
        self.assertEqual(grid[0][1].value(), 20)
        self.assertEqual(grid[0][2].value(), 30)

    def test_set_nested_arrays(self):
        grid = Grid()
        grid[0] = [[10], [20], [31, 32, 33]]

        self.assertEqual(grid[0][0][0].value(), 10)
        self.assertEqual(grid[0][1][0].value(), 20)

        self.assertEqual(grid[0][2][0].value(), 31)
        self.assertEqual(grid[0][2][1].value(), 32)
        self.assertEqual(grid[0][2][2].value(), 33)
