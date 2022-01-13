class Cell:
    """Class representing the grid."""

    def __init__(self, _root=None, _children=[None, {}], _location=()):
        self._children = _children
        self._root = _root if _root else self
        self._location = _location

    def __setitem__(self, index, value):
        if isinstance(value, list):

            if isinstance(index, slice):
                step = index.step or 1
                start = index.start or index.stop - (len(value) * step) + 1
                stop = index.stop or index.start + (len(value) * step) - 1

                if (stop - start) / step + 1 != len(value):
                    print((stop - start) / step, len(value))
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
            if index not in self._children[1]:
                self._children[1][index] = [value, {}]
            else:
                self._children[1][index][0] = value

    def __delitem__(self, index):
        del self._children[1][index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            step = index.step or 1
            start = index.start or min(self._children[1].keys())
            stop = index.stop or max(self._children[1].keys())
            return [self[value_index] for value_index in range(start, stop + 1, step)]
        else:
            if index not in self._children[1]:
                if self._children[0] is not None:
                    raise Exception("Object is not subscriptable")
                self._children[1][index] = [
                    None,
                    {},
                ]  # wait to set this until we are storing a value?
            return Cell(self._root, self._children[1][index], self._location + (index,))

    def __iter__(self):
        if self._children[1]:
            for index in self._children[1].keys():
                yield from Cell(
                    self._root, self._children[1][index], self._location + (index,)
                ).__iter__()
        else:
            yield self

    def __len__(self):
        return len(self._children[1])

    def __contains__(self, index):
        if index in self._children[1]:
            return True
        for value in self._children[1].values():
            if value[0] == index:
                return True
        return False

    def __str__(self):
        if self._children[1]:
            return (
                "["
                + ",".join(
                    [
                        Cell(
                            self._root,
                            self._children[1][index],
                            self._location + (index,),
                        ).__str__()
                        for index in self._children[1].keys()
                    ]
                )
                + "]"
            )
        else:
            return str(self._children[0])

    def value(self):
        return self._children[0]

    def coordinate(self):
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

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self._children == other._children
        else:
            return self._children[0] == other

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
        super().__init__(self, _children=(None, {}), _location=())
