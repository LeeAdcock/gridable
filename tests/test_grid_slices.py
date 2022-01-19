import unittest
from gridable import Grid


class TestNodeSlices(unittest.TestCase):
    def test_put_slice_start_stop(self):
        grid = Grid()
        grid[0][5:6] = [7, 8]

        self.assertEqual(grid[0][5].value(), 7)
        self.assertEqual(grid[0][6].value(), 8)

    def test_put_slice_start(self):
        grid = Grid()
        grid[0][5:] = [7, 8]

        self.assertEqual(grid[0][5].value(), 7)
        self.assertEqual(grid[0][6].value(), 8)

    def test_put_slice_stop(self):
        grid = Grid()
        grid[0][:6] = [7, 8]

        self.assertEqual(grid[0][5].value(), 7)
        self.assertEqual(grid[0][6].value(), 8)

    def test_put_slice_step(self):
        grid = Grid()
        grid[0][5:7:2] = [7, 8]

        self.assertEqual(grid[0][5].value(), 7)
        self.assertEqual(grid[0][7].value(), 8)

    def test_put_slice_invalid_too_small(self):
        grid = Grid()
        exception = False
        try:
            grid[0][5:7:2] = [7, 8, 9]
        except:
            exception = True
        self.assertTrue(exception)

    def test_put_slice_invalid_too_big(self):
        grid = Grid()
        exception = False
        try:
            grid[0][5:700:2] = [7, 8, 9]
        except:
            exception = True
        self.assertTrue(exception)

    def test_get_slice_start(self):
        grid = Grid()
        grid[0] = [1, 2, 3, 4, 5]

        out = list(grid[0][3:])

        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].value(), 4)
        self.assertEqual(out[1].value(), 5)

    def test_get_slice_stop(self):
        grid = Grid()
        grid[0] = [1, 2, 3, 4, 5]

        out = list(grid[0][:2])

        self.assertEqual(len(out), 3)
        self.assertEqual(out[0].value(), 1)
        self.assertEqual(out[1].value(), 2)
        self.assertEqual(out[2].value(), 3)

    def test_get_slice_step(self):
        grid = Grid()
        grid[0] = [1, 2, 3, 4, 5]

        out = list(grid[0][::2])

        self.assertEqual(len(out), 3)
        self.assertEqual(out[0].value(), 1)
        self.assertEqual(out[1].value(), 3)
        self.assertEqual(out[2].value(), 5)

    def test_put_iterable_slice(self):
        grid = Grid()
        grid[0][10:] = range(5, 7)

        self.assertEqual(grid[0][10].value(), 5)
        self.assertEqual(grid[0][11].value(), 6)
