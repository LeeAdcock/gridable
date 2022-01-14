from gridable.threadlock import GridModifyLock, GridReadLock
import functools


class Cell:
    """Class representing a location or span in the grid."""

    def __init__(self, _root, _coordinates=()):
        self._root = _root
        self._coordinates = _coordinates

    """Sets the content of a grid cell."""

    @GridModifyLock
    def __setitem__(self, index, value):
        if isinstance(value, list):

            if isinstance(index, slice):
                step = index.step or 1
                start = index.start or index.stop - (len(value) * step) + 1
                stop = index.stop or index.start + (len(value) * step) - 1

                if (stop - start) / step + 1 != len(value):
                    raise Exception(
                        "Invalid slice size",
                    )

                indexes = list(
                    range(
                        start,
                        stop + 1,
                        step,
                    )
                )
                for (value_index, value) in enumerate(value):
                    self[indexes[value_index]] = value
            else:
                for (value_index, value) in enumerate(value):
                    self[index][value_index] = value

        else:
            self._persist()
            self._get_content()[index] = value

    """Deletes the contents of a grid cell."""

    @GridModifyLock
    def __delitem__(self, index):
        del self._get_content()[index]

    """Get the contents of a grid cell."""

    def __getitem__(self, index):
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

    """ Creates a generator that returns nested grid cells """

    @GridReadLock
    def __iter__(self):
        def generator(root, value, location):
            if isinstance(value, dict):
                for index in value:
                    yield from generator(root, value[index], location + (index,))
            else:
                yield Cell(root, location)

        yield from generator(self._root, self._get_content(), self._coordinates)

    """ Returns the number of included values. Specifically does not count None values."""

    @GridReadLock
    def __len__(self):
        content = self._get_content()
        return len(content) if isinstance(content, dict) else 1

    """ Returns a boolean indicating if the provided value is within nested grid cells"""

    @GridReadLock
    def __contains__(self, index):
        content = self._get_content()
        if not isinstance(content, dict):
            return False
        return (index in content) or (index in content.values())

    """ Return a string representation of this cell"""

    @GridReadLock
    def __str__(self):
        def crawl_str(content):
            return (
                str(content)
                if not isinstance(content, dict)
                else "[" + ",".join([crawl_str(x) for x in content.values()]) + "]"
            )

        return crawl_str(self._get_content())

    """ Return a boolean indicating if this cell is equal to another cell or its value. """

    @GridReadLock
    def __eq__(self, other):
        content = self._get_content()
        return (
            content == other._get_content()
            if isinstance(other, Cell)
            else content == other
        )

    """ Get the inner persisted value at the current cell location, or None if it isn't persisted. """

    def _get_content(self):
        return functools.reduce(
            lambda a, b: a[b] if a is not None and b in a else None,
            (self._root,) + self._coordinates,
        )

    """ Persist the location of the current cell to enable storing its value. """

    @GridModifyLock
    def _persist(self):
        cursor = self._root
        for value in self._coordinates:
            if value not in cursor:
                cursor[value] = {}
            cursor = cursor[value]

    """ Returns the value stored in the current cell, or None. """

    @GridReadLock
    def value(self):
        content = self._get_content()
        return content if not isinstance(content, dict) else None

    """ Returns the coordinates of the current cell, or None. """

    def coordinates(self):
        return self._coordinates

    """ Returns the grid distance between coordinates of the current and provided cell. """

    def distance(self, cell):
        if not len(self._coordinates) == len(cell._coordinates):
            raise Exception("Unequal number of dimensions")
        return sum(
            [
                abs(self._coordinates[index] - cell._coordinates[index])
                for index, value in enumerate(self._coordinates)
            ]
        )

    """ Returns a generator that provides all neighboring cells at the given distance"""

    def neighbors(self, include_empty=True, distance=1):
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
