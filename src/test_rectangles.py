from rectangle_analyzer import RectangleAnalyzer


# -----------------------------
# Normal cases
# -----------------------------

def test_non_overlapping_rectangles():
    rectangles = [
        {"x": 0, "y": 0, "width": 2, "height": 2},
        {"x": 3, "y": 3, "width": 2, "height": 2},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    assert analyzer.find_overlaps() == []
    assert analyzer.calculate_coverage_area() == 8
    assert analyzer.is_point_covered(1, 1) is True
    assert analyzer.is_point_covered(6, 5) is False


def test_simple_overlap():
    rectangles = [
        {"x": 0, "y": 0, "width": 4, "height": 4},
        {"x": 2, "y": 2, "width": 4, "height": 4},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    overlaps = analyzer.find_overlaps()
    assert overlaps == [(0, 1)]

    overlap_regions = analyzer.get_overlap_regions()
    assert overlap_regions[0]["region"]["x"] == 2
    assert overlap_regions[0]["region"]["y"] == 2
    assert overlap_regions[0]["region"]["width"] == 2
    assert overlap_regions[0]["region"]["height"] == 2


def test_negative_coordinates_no_overlap():
    rectangles = [
        {"x": -10, "y": -10, "width": 3, "height": 3},
        {"x": -3, "y": -3, "width": 2, "height": 2},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    assert analyzer.find_overlaps() == []
    assert analyzer.calculate_coverage_area() == 13

def test_negative_overlap():
    rectangles = [
        {"x": -5, "y": -5, "width": 4, "height": 4},
        {"x": -3, "y": -3, "width": 4, "height": 4},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    overlaps = analyzer.find_overlaps()
    assert overlaps == [(0, 1)]

    overlap_regions = analyzer.get_overlap_regions()
    region = overlap_regions[0]["region"]

    assert region["width"] == 2
    assert region["height"] == 2

def test_crossing_origin():
    rectangles = [
        {"x": -2, "y": -2, "width": 4, "height": 4},
        {"x": -1, "y": -1, "width": 2, "height": 2},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    assert analyzer.is_point_covered(0, 0) is True
    assert analyzer.is_point_covered(-3, -3) is False

# -----------------------------
# Boundary cases (geometry)
# -----------------------------

def test_touching_edges_no_overlap():
    rectangles = [
        {"x": 0, "y": 0, "width": 2, "height": 2},
        {"x": 2, "y": 0, "width": 2, "height": 2},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    # touching edges should not count as overlap
    assert analyzer.find_overlaps() == []


def test_nested_rectangles():
    rectangles = [
        {"x": 0, "y": 0, "width": 10, "height": 10},
        {"x": 2, "y": 2, "width": 2, "height": 2},
        {"x": 1, "y": 1, "width": 4, "height": 4},

    ]

    analyzer = RectangleAnalyzer(rectangles)

    assert analyzer.find_overlaps() == [(0,1), (0,2),(1,2)]
    assert analyzer.calculate_coverage_area() == 100


# -----------------------------
# Edge cases (input structure)
# -----------------------------

def test_empty_input():
    analyzer = RectangleAnalyzer([])

    assert analyzer.find_overlaps() == []
    assert analyzer.calculate_coverage_area() == 0.0


def test_single_rectangle():
    rectangles = [{"x": 0, "y": 0, "width": 5, "height": 5}]
    analyzer = RectangleAnalyzer(rectangles)

    assert analyzer.find_overlaps() == []
    assert analyzer.calculate_coverage_area() == 25


def test_zero_area_rectangle():
    rectangles = [
        {"x": 1, "y": 0, "width": 0, "height": 5},
        {"x": 0, "y": 0, "width": 3, "height": 3},
    ]

    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == []
    assert analyzer.calculate_coverage_area() == 9


# -----------------------------
# Max overlap point
# -----------------------------

def test_max_overlap_point():
    rectangles = [
        {"x": 0, "y": 0, "width": 4, "height": 4},
        {"x": 2, "y": 2, "width": 4, "height": 4},
        {"x": 1, "y": 1, "width": 4, "height": 4},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    result = analyzer.find_max_overlap_point()

    assert result["count"] == 3
    assert analyzer.is_point_covered(result["x"], result["y"])

def test_max_overlap_point_matreshka_rectangle():
    rectangles = [
        {"x": 0, "y": 0, "width": 10, "height": 10},
        {"x": 1, "y": 1, "width": 8, "height": 8},
        {"x": 2, "y": 2, "width": 6, "height": 6},
        {"x": 3, "y": 3, "width": 4, "height": 4},
        {"x": 4, "y": 4, "width": 2, "height": 2},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    result = analyzer.find_max_overlap_point()

    assert result["count"] == 5
    assert analyzer.is_point_covered(result["x"], result["y"])

def test_nested_negative_rectangles():
    rectangles = [
        {"x": -10, "y": -10, "width": 20, "height": 20},
        {"x": -8, "y": -8, "width": 16, "height": 16},
        {"x": -6, "y": -6, "width": 12, "height": 12},
        {"x": -4, "y": -4, "width": 8, "height": 8},
        {"x": -2, "y": -2, "width": 4, "height": 4},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    result = analyzer.find_max_overlap_point()

    assert result["count"] == 5
    assert analyzer.is_point_covered(result["x"], result["y"])


# -----------------------------
# Stats function
# -----------------------------

def test_stats_output():
    rectangles = [
        {"x": 0, "y": 0, "width": 4, "height": 4},
        {"x": 2, "y": 2, "width": 4, "height": 4},
    ]

    analyzer = RectangleAnalyzer(rectangles)

    stats = analyzer.get_stats()

    assert stats["total_rectangles"] == 2
    assert stats["overlapping_pairs"] == 1
    assert stats["total_area"] > 0


# -----------------------------
# Stress case
# -----------------------------

def test_many_rectangles_stress():
    rectangles = []

    for i in range(50):
        rectangles.append({
            "x": i,
            "y": i,
            "width": 10,
            "height": 10
        })

    analyzer = RectangleAnalyzer(rectangles)

    area = analyzer.calculate_coverage_area()
    assert analyzer.get_stats()['total_rectangles'] == 50
    assert area > 500

def test_many_negative_rectangles():
    rectangles = []

    for i in range(30):
        rectangles.append({
            "x": -i,
            "y": -i,
            "width": 10,
            "height": 10
        })

    analyzer = RectangleAnalyzer(rectangles)

    area = analyzer.calculate_coverage_area()
    assert analyzer.get_stats()['total_rectangles'] == 30
    assert area > 500