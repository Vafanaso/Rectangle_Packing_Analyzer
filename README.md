# Rectangle Analyzer

Rectangle Analyzer is a small Python project that analyzes axis-aligned rectangles on a 2D plane. The tool can detect overlaps between rectangles, compute overlap regions, calculate the total covered area, and find points with the maximum overlap.

The project is implemented in Python and includes automated tests.

## Features

The `RectangleAnalyzer` class supports the following operations:

**find_overlaps()**
Finds all pairs of rectangles that overlap.

**get_overlap_regions()**
Computes the intersection region for each overlapping pair of rectangles.

**calculate_coverage_area()**
Calculates the total area covered by all rectangles, counting overlaps only once. This is implemented using the Sweep Line algorithm, a common computational geometry technique.

**is_point_covered(x, y)**
Checks whether a point lies inside or on the boundary of any rectangle.

**find_max_overlap_point()**
Finds a point that is covered by the maximum number of rectangles.

**get_stats()**
Returns summary statistics about the rectangle configuration.

## Geometry Rules

The implementation follows these geometric conventions:

1. **Points on edges or corners are considered part of the rectangle.**

2. **Rectangles that only touch at an edge or corner are not considered overlapping**,  
   because their intersection area is zero.

3. In `get_stats()`, **overlap_area** is defined as the **sum of all pairwise overlap regions**,  
   exactly as stated in the method docstring (`sum of all overlap regions`).  
   This means that if three rectangles overlap in the same place, that region may contribute
   multiple times (once for each overlapping pair).

## Rectangle Format

Rectangles are defined as dictionaries with the following keys:

```
{
    "x": number,
    "y": number,
    "width": number,
    "height": number
}
```

Where:

* `x`, `y` represent the bottom-left corner of the rectangle
* `width` is the rectangle width
* `height` is the rectangle height

Example:

```
rectangles = [
    {"x": 0, "y": 0, "width": 4, "height": 4},
    {"x": 2, "y": 2, "width": 4, "height": 4}
]
```

## Installation

The project uses `pyproject.toml` to define its Python environment.

Install dependencies using `uv`:

```
uv sync
```

## Running Tests

The project includes a test suite that validates different scenarios including:

* normal rectangle configurations
* boundary cases
* negative coordinates
* edge cases
* stress tests

Run the tests with:

```
uv run pytest
```

## Example Usage

```
from rectangle_analyzer import RectangleAnalyzer

rectangles = [
    {"x": 0, "y": 0, "width": 4, "height": 4},
    {"x": 2, "y": 2, "width": 4, "height": 4}
]

analyzer = RectangleAnalyzer(rectangles)

print(analyzer.find_overlaps())
print(analyzer.calculate_coverage_area())
print(analyzer.find_max_overlap_point())
print(analyzer.get_stats())
```

## Requirements

* Python 3.10 or newer

Dependencies are defined in `pyproject.toml`.

