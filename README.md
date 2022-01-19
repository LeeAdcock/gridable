*Gridable is an easy to use, in memory, infinitely scaled data grid. It is perfect for prototyping, exploring, and quick implementation in Python applications.* The library is written completely in Python, supporting 3.6+. 

In Gridable, data grids are made of cells that can be indexed along any number of dimensions. Each dimension can be referenced without limits, enabling the creation of very large grids without tedious initialization. Gridable is thread safe for multi-threaded applications and easily handles grids with tens to hundreds of thousands of cells.

Storing and retreiving values in the grid can be done through direct indexing, or through slices, arrays, and generators for efficient handling of very large datasets.

## Installation

The Gridable library can easily be installed with pip using `pip install gridable`.

## Creating a Grid

Creating a grid can be done through the constructor. Grids have no maximum dimensions, but are populated with `None` values at creation.

```
grid = Grid()
```

Storing values into the grid can be done similary to how you might work with nested arrays, but have the flexibility of using ranges to specify storage location and can consume iterable values. The number of dimensions do not have to be predefined, or consistant.

```
# Single dimension (number line)
grid[5] = 6

# Two dimensions (matrix)
grid[6][7] = 8

# Or any number of dimensions
grid[7][8][9][10] = 11
```

Values placed into the grid can be single values, like above, or any iterable.

```
grid[5] = [6, 7, 8]
grid[6] = range(7, 9)
```

The destination location when setting values can be a slice, which allows defining the start index, and/or the end index, and optionaly the  increment step. Values not included in the slice will retain their existing value.

```
grid[7][5:9:2] = [6, 7, 8]
```

## Working with Cells

When referencing values inside the grid, a `Cell` instance will be returned. This wraps the value and provides a number of convenience methods.  Although many operations like cell comparisons and equality work on the cell value, as would be expected, the `value()` method returns the cell content when it is needed explicity.

```
grid[6][7].value()
```

Other convenience methods return the cell's coordinates as a tuple, or provide easy access to retrieivng a list of cell neighbors or distances.

```
grid[6][7].coordinates()
grid[6][7].distance(grid[7][10])
grid[6][7].neighbors()

```

Processing through the grid can be done through iteration. All cells function as an iterator for the values they contain, whether it's a single value, or one or more inner dimensions. If a slice is used to specify the cell location, the iterator will return those cells specifically, skipping over cells not included in the slice.

```
for cell in grid[6]:
    print(cell)

for even_cells in grid[2::2]:
    print(cell)
````