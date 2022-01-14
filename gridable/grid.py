class Cell:
    """Class representing the grid."""

    def __init__(self, _root=None, _parent=None, _children=None, _location=()):
        self._parent = _parent
        self._children = _children
        self._root = _root if _root else self
        self._location = _location

    def _persist(self, index):
        if self._parent:
            self._children = self._parent._persist(self._location[-1])

        if self._children is None:
            self._children = {}

        if index not in self._children:
            self._children[index] = {}

        return self._children[index]

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
            if self._children is None:
                if self._parent:
                    self._children = self._parent._persist(self._location[-1])
                else:
                    self._root = {}
                    self._children = {}
            self._children[index] = value

    def __delitem__(self, index):
        if isinstance(self._children, dict):
            del self._children[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            step = index.step or 1
            start = index.start or min(self._children.keys())
            stop = index.stop or max(self._children.keys())
            return [self[value_index] for value_index in range(start, stop + 1, step)]
        else:
            if self._children is None:
                return Cell(self._root, self, None, self._location + (index,))
            else:
                if isinstance(self._children, dict):
                    return Cell(
                        self._root,
                        self,
                        self._children[index] if index in self._children else None,
                        self._location + (index,),
                    )
                else:
                    raise Exception("Not subspcriptable")

    def __iter__(self):
        if isinstance(self._children, dict):
            for index in self._children.keys():
                yield from Cell(
                    self._root, self, self._children[index], self._location + (index,)
                ).__iter__()
        else:
            yield self

    def __len__(self):
        return len(self._children) if isinstance(self._children, dict) else 1

    def __contains__(self, index):
        if isinstance(self._children, dict):
            if index in self._children:
                return True
            for value in self._children.values():
                if value == index:
                    return True
            return False
        else:
            return index == self._children

    def __str__(self):
        return str(self._children)

    def value(self):
        if isinstance(self._children, dict):
            return None  # error?
        else:
            return self._children

    def size(self):
        def _get_size(value):
            size = 0
            if isinstance(value, dict):
                for child in value.values():
                    size += _get_size(child) if isinstance(child, dict) else 1
            return size

        return _get_size(self._children)

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
            return self._children == other

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
        super().__init__(self, _children=None, _location=())


grid = Grid()
# grid[5] = [2, 3]
# grid[5][2] = 4
grid[6][1] = 4
print(grid[6][1])

print(grid._children)
print("size", grid.size())
