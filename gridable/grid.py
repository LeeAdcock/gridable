import functools


class Cell:
    """Class representing a location in the grid."""

    def __init__(self, _root, _location=()):
        self._root = _root
        self._location = _location

    def _get_value(self):
        return functools.reduce(
            lambda a, b: a[b] if a is not None and b in a else None,
            (self._root,) + self._location,
        )

    def _persist(self):
        cursor = self._root
        for value in self._location:
            if value not in cursor:
                cursor[value] = {}
            cursor = cursor[value]

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
            self._get_value()[index] = value

    def __delitem__(self, index):
        del self._get_value()[index]

    def __getitem__(self, index):
        value = self._get_value()
        if isinstance(index, slice):
            step = index.step or 1
            start = index.start or min(value.keys())
            stop = index.stop or max(value.keys())
            return [self[value_index] for value_index in range(start, stop + 1, step)]
        else:
            if value is not None and not isinstance(value, dict):
                raise Exception("Not subscriptable")
            return Cell(self._root, self._location + (index,))

    def __iter__(self):
        def _crawl(root, value, location):
            if isinstance(value, dict):
                for index in value:
                    yield from _crawl(root, value[index], location + (index,))
            else:
                yield Cell(root, location)

        yield from _crawl(self._root, self._get_value(), self._location)

    def __len__(self):
        data = self._get_value()
        return len(data) if isinstance(data, dict) else 1

    def __contains__(self, index):
        data = self._get_value()
        if not isinstance(data, dict):
            return False
        return (index in data) or (index in data.values())

    def __str__(self):
        return str(self.value())

    def __eq__(self, other):
        data = self._get_value()
        return data == other._get_value() if isinstance(other, Cell) else data == other

    def value(self):
        value = self._get_value()
        return value if not isinstance(value, dict) else None

    def coordinates(self):
        return self._location

    def distance(self, cell):
        if not len(self._location) == len(cell._location):
            raise Exception("Unequal number of dimensions")
        return sum(
            [
                abs(self._location[index] - cell._location[index])
                for index, value in enumerate(self._location)
            ]
        )

    def neighbors(self, include_empty=True, distance=1):
        def _neighbors(cell, location, index):
            if index > len(location) - 1:
                if cell.value() is not None or include_empty:
                    yield cell
            else:
                for delta in range(-distance, distance + 1):
                    new_location = list(location)
                    new_location[index] += delta
                    yield from _neighbors(
                        cell[new_location[index]], new_location, index + 1
                    )

        yield from _neighbors(self._root, self._location, 0)


class Grid(Cell):
    """Class representing the grid."""

    def __init__(self):
        super().__init__(_root={})
