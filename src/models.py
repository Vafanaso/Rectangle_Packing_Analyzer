from collections import Counter

class RectangleAnalyzer:

    def __init__(self, rectangles: list[dict]):
        """
        Initialize analyzer with list of rectangles.
        Each rectangle is a dict with keys: x, y, width, height
        """
        self.rectangles = rectangles

    def _boundries(self,rectangle:dict)-> dict[str,float]:
        """
        A helper function that returns boundries of the given rectangle

        """
        xmin = float(rectangle['x'])
        xmax = float(xmin + rectangle['width'])
        ymin = float(rectangle['y'])
        ymax = float(ymin + rectangle['height'])
        boundries = {'xmin': xmin,'xmax' : xmax, 'ymin': ymin,'ymax' : ymax}
        return boundries

    def _rectangle_area(self, rectangle:dict) -> float:
        area:float = 0

        boundries = self._boundries(rectangle)

        x_len:float = boundries['xmax'] - boundries['xmin']
        y_len:float = boundries['ymax'] - boundries['ymin']

        area = x_len * y_len

        return area


    def find_overlaps(self) -> list[tuple[int,int]]:
        """
        Find all pairs of overlapping rectangles.
        Returns: List of tuples (i, j) where i < j are indices
        Example: [(0, 1), (0, 2), (1, 2)]
        """
        rectangles = self.rectangles
        res: list[tuple[int,int]] = []
        if len(rectangles) != 0:
             for i in range(len(rectangles)):
                 for j in range(i + 1, len(rectangles)):

                    ibound = self._boundries(rectangles[i])
                    jbound = self._boundries(rectangles[j])

                    # ixmin = rectangles[i]['x']
                    # ixmax = ixmin + rectangles[i]['width']
                    # iymin = rectangles[i]['y']
                    # iymax = iymin + rectangles[i]['height']
                    # jxmin = rectangles[j]['x']
                    # jxmax = jxmin + rectangles[j]['width']
                    # jymin = rectangles[j]['y']
                    # jymax = jymin + rectangles[j]['height']


                    if min(ibound['xmax'], jbound['xmax']) > max(ibound['xmin'], jbound['xmin']):
                        if min(ibound['ymax'], jbound['ymax']) > max(ibound['ymin'], jbound['ymin']):
                            res.append((i,j))
        return res




    def calculate_coverage_area(self) -> float:
        """
            Calculate the total area covered by all rectangles using the Sweep Line algorithm.

            This method computes the union area of axis-aligned rectangles, meaning
            overlapping regions are counted only once. The implementation is based on
            the classical Sweep Line (or Line Sweep) technique from computational
            geometry, which is commonly used to solve rectangle union area problems.

            Algorithm
            ---------
            A horizontal sweep line moves from the bottom to the top of the plane.
            For each rectangle two events are generated:
                - an OPEN event at the rectangle's bottom edge (ymin)
                - a CLOSE event at the rectangle's top edge (ymax)

            While sweeping, the algorithm maintains a set of active horizontal
            intervals representing x-ranges of rectangles intersecting the current
            sweep line.

            Between two consecutive y-events, the active intervals are merged to
            determine the total covered width along the x-axis. The area contributed
            by that horizontal strip is calculated as:

                covered_width * (y_current - y_previous)

            The total area is accumulated until all events have been processed.

            Returns
            -------
            float
                Total union area covered by all rectangles.
            """
        OPEN, CLOSE = 1, -1
        events: list[tuple[float, int, float, float]] = []  # (y, type, x1, x2)

        # Build sweep events
        for rect in self.rectangles:
            b = self._boundries(rect)
            x1, x2 = b["xmin"], b["xmax"]
            y1, y2 = b["ymin"], b["ymax"]
            if x1 >= x2 or y1 >= y2:
                continue
            events.append((y1, OPEN, x1, x2))
            events.append((y2, CLOSE, x1, x2))

        if not events:
            return 0.0

        events.sort(key=lambda e: e[0])  # sort by y
        active: Counter[tuple[float, float]] = Counter()

        def covered_x_length() -> float:
            """Total covered x-length from active intervals (merged)."""
            intervals = [(x1, x2) for (x1, x2), c in active.items() if c > 0 and x1 < x2]
            if not intervals:
                return 0.0

            intervals.sort()
            total = 0.0
            cur_l, cur_r = intervals[0]
            for l, r in intervals[1:]:
                if l > cur_r:
                    total += cur_r - cur_l
                    cur_l, cur_r = l, r
                else:
                    cur_r = max(cur_r, r)
            total += cur_r - cur_l
            return total

        area = 0.0
        prev_y = events[0][0]
        i = 0
        n = len(events)

        while i < n:
            y = events[i][0]
            area += covered_x_length() * (y - prev_y)

            # apply all events at this same y
            while i < n and events[i][0] == y:
                _, typ, x1, x2 = events[i]
                active[(x1, x2)] += typ
                if active[(x1, x2)] == 0:
                    del active[(x1, x2)]
                i += 1

            prev_y = y

        return area


    def get_overlap_regions(self) -> list[dict]:
        """
        Find actual overlap regions between rectangles.
        Returns: List of dicts containing:
        - 'rect_indices': tuple of rectangle indices
        - 'region': dict with x, y, width, height of overlap
        """
        overlaps:list[tuple[int,int]] = self.find_overlaps()
        res:list[dict] =[]


        for item in overlaps:

            ibound:dict = self._boundries(self.rectangles[item[0]])
            jbound:dict = self._boundries(self.rectangles[item[1]])

            x = max(ibound['xmin'], jbound['xmin'])
            y = max(ibound['ymin'], jbound['ymin'])
            width = min(ibound['xmax'], jbound['xmax']) - x
            height = min(ibound['ymax'], jbound['ymax']) - y
            region:dict = {'x':x, 'y':y, 'width':width, 'height':height}

            res.append({'rect_indices': item, 'region':region})
        return res



    def is_point_covered(self, x: int | float, y: int | float) -> bool:
        """
        Check if a point is covered by any rectangle.
        Returns: boolean
        """


        for rect in self.rectangles:
            rect_bound = self._boundries(rect)
            if rect_bound['xmin'] < x < rect_bound['xmax']:
                if rect_bound['ymin'] < y < rect_bound['ymax']:
                    return True

        return False


    def find_max_overlap_point(self) -> dict:
        """
        Find a point covered by the maximum number of rectangles.

        The method evaluates candidate points derived from rectangle
        boundary coordinates. Overlap counts only change at rectangle
        edges, therefore it is sufficient to test points between these
        boundaries.

        Returns
        -------
        dict
            {
                'x': float,
                'y': float,
                'count': int
            }
            where (x, y) is a point covered by the maximum number
            of rectangles and 'count' is the number of rectangles
            covering that point.
        """

        xs: set[float] = set()
        ys: set[float] = set()

        # collect all boundary coordinates
        for rect in self.rectangles:
            b = self._boundries(rect)
            xs.add(b["xmin"])
            xs.add(b["xmax"])
            ys.add(b["ymin"])
            ys.add(b["ymax"])

        xs_sorted:list[float]  = sorted(xs)
        ys_sorted:list[float]  = sorted(ys)

        max_count = 0
        best_x = 0.0
        best_y = 0.0

        # test midpoints between boundaries
        for i in range(len(xs_sorted) - 1):
            for j in range(len(ys_sorted) - 1):

                x = (xs_sorted[i] + xs_sorted[i + 1]) / 2
                y = (ys_sorted[j] + ys_sorted[j + 1]) / 2

                count = 0
                for rect in self.rectangles:
                    b = self._boundries(rect)
                    if b["xmin"] <= x <= b["xmax"] and b["ymin"] <= y <= b["ymax"]:
                        count += 1

                if count > max_count:
                    max_count = count
                    best_x = x
                    best_y = y

        return {
            "x": best_x,
            "y": best_y,
            "count": max_count
        }

    def get_stats(self) -> dict:
        """
        Get coverage statistics.
        Returns: dict with:
        - 'total_rectangles': int
        - 'overlapping_pairs': int
        - 'total_area': float (union area)
        - 'overlap_area': float (sum of all overlap regions)
        - 'coverage_efficiency': float (total_area /

        sum_of_individual_areas)

        """

        total_rectangles:int = len(self.rectangles)
        overlapping_pairs:int = len(self.find_overlaps())
        total_area:float = self.calculate_coverage_area()
        overlap_area: float = 0
        sum_of_individual_areas:float = 0
        coverage_efficiency: float = 0

        for rectangle in self.rectangles:

            area: float = self._rectangle_area(rectangle)
            sum_of_individual_areas += area

        for dicts in self.get_overlap_regions():

            area:float = self._rectangle_area(dicts['region'])
            overlap_area += area

        coverage_efficiency = total_area / sum_of_individual_areas


        stats:dict ={'total_ractangles':total_rectangles,
                     'overlapping_pairs': overlapping_pairs,
                     'total_area': total_area,
                     'overlap_area':overlap_area,
                     'coverage_efficiency': coverage_efficiency
                      }

        return stats
