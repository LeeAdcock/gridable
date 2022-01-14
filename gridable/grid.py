from gridable.threadlock import GridModifyLock, GridReadLock
import functools
from collections.abc import Iterable


class Cell:
    """Class representing a location or span in the grid."""

    def __init__(self, _root, _coordinates=()):
        self._root = _root
        self._coordinates = _coordinates

    @GridModifyLock
    def __setitem__(self, index, value):
        """Sets the content of a grid cell."""
        if isinstance(value, Iterable):

            if isinstance(index, slice):
                step = index.step or 1
                start = index.start or index.stop - (len(value) * step) + 1
                stop = index.stop or index.start + (len(value) * step) - 1

                if (stop - start) / step + 1 != len(value):
                    raise Exception(
                        "Invalid slice size",
                    )

                for (source_index, destination_index) in enumerate(
                    range(
                        start,
                        stop + 1,
                        step,
                    )
                ):
                    self[destination_index] = value[source_index]
            else:
                for (value_index, value) in enumerate(value):
                    self[index][value_index] = value

        else:
            self._persist()
            self._get_content()[index] = value

    @GridModifyLock
    def __delitem__(self, index):
        """Deletes the contents of a grid cell."""
        del self._get_content()[index]

    def __getitem__(self, index):
        """Get the contents of a grid cell."""
        content = self._get_content()
        if isinstance(index, slice):
            step = index.step or 1
            start = index.start or min(content.keys())
            stop = index.stop or max(content.keys())

            @GridReadLock
            def generator():
                for value_index in range(start, stop + 1, step):
                    yield self[value_index]

            return generator()
        else:
            if content is not None and not isinstance(content, dict):
                raise Exception("Not subscriptable")
            return Cell(self._root, self._coordinates + (index,))

    @GridReadLock
    def __iter__(self):
        """Creates a generator that returns nested grid cells"""

        def generator(root, value, location):
            if isinstance(value, dict):
                for index in value:
                    yield from generator(root, value[index], location + (index,))
            else:
                yield Cell(root, location)

        yield from generator(self._root, self._get_content(), self._coordinates)

    @GridReadLock
    def __len__(self):
        """Returns the number of included values. Specifically does not count None values."""
        content = self._get_content()
        return len(content) if isinstance(content, dict) else 1

    @GridReadLock
    def __contains__(self, index):
        """Returns a boolean indicating if the provided value is within nested grid cells"""
        content = self._get_content()
        if not isinstance(content, dict):
            return False
        return (index in content) or (index in content.values())

    @GridReadLock
    def __str__(self):
        """Return a string representation of this cell"""

        def crawl_str(content):
            return (
                str(content)
                if not isinstance(content, dict)
                else "[" + ",".join([crawl_str(x) for x in content.values()]) + "]"
            )

        return crawl_str(self._get_content())

    @GridReadLock
    def __eq__(self, other):
        """Return a boolean indicating if this cell is equal to another cell or its value."""
        content = self._get_content()
        return (
            content == other._get_content()
            if isinstance(other, Cell)
            else content == other
        )

    def _get_content(self):
        """Get the inner persisted value at the current cell location, or None if it isn't persisted."""
        return functools.reduce(
            lambda a, b: a[b] if a is not None and b in a else None,
            (self._root,) + self._coordinates,
        )

    @GridModifyLock
    def _persist(self):
        """Persist the location of the current cell to enable storing its value."""
        cursor = self._root
        for value in self._coordinates:
            if value not in cursor:
                cursor[value] = {}
            cursor = cursor[value]

    @GridReadLock
    def value(self):
        """Returns the value stored in the current cell, or None."""
        content = self._get_content()
        return content if not isinstance(content, dict) else None

    def coordinates(self):
        """Returns the coordinates of the current cell, or None."""
        return self._coordinates

    def distance(self, cell):
        """Returns the grid distance between coordinates of the current and provided cell."""
        if not len(self._coordinates) == len(cell._coordinates):
            raise Exception("Unequal number of dimensions")
        return sum(
            [
                abs(self._coordinates[index] - cell._coordinates[index])
                for index, value in enumerate(self._coordinates)
            ]
        )

    def neighbors(self, include_empty=True, distance=1):
        """Returns a generator that provides all neighboring cells at the given distance"""

        def _neighbors(cell, location, index):
            if index > len(location) - 1:
                if cell.value() is not None or include_empty:
                    yield cell
            else:
                for delta in range(-distance, distance + 1):
                    new_coordinates = list(location)
                    new_coordinates[index] += delta
                    yield from _neighbors(
                        cell[new_coordinates[index]], new_coordinates, index + 1
                    )

        yield from _neighbors(self._root, self._coordinates, 0)


class Grid(Cell):
    """Class representing the grid."""

    def __init__(self):
        super().__init__(_root={})
