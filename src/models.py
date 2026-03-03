class RectangleAnalyzer:

    def __init__(self, rectangles: list[dict]):
        """
        Initialize analyzer with list of rectangles.
        Each rectangle is a dict with keys: x, y, width, height
        """
        self.rectangles = rectangles

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
                    ixmin = rectangles[i]['x']
                    ixmax = ixmin + rectangles[i]['width']
                    iymin = rectangles[i]['y']
                    iymax = iymin + rectangles[i]['height']
                    jxmin = rectangles[j]['x']
                    jxmax = jxmin + rectangles[j]['width']
                    jymin = rectangles[j]['y']
                    jymax = jymin + rectangles[j]['height']


                    if min(ixmax, jxmax) > max(ixmin, jxmin):
                        if min(iymax, jymax) > max(iymin, jymin):
                            res.append((i,j))
        return res





    def calculate_coverage_area(self) -> float:
        """
        Calculate total area covered by all rectangles.
        Overlapping areas should be counted only once.
        Returns: float/int representing total area
        """
        pass

    def get_overlap_regions(self) -> list[dict]:
        """
        Find actual overlap regions between rectangles.
        Returns: List of dicts containing:
        - 'rect_indices': tuple of rectangle indices
        - 'region': dict with x, y, width, height of overlap
        """
        # overlaps:list[tuple[int,int]] = self.find_overlaps()
        # res:list[dict] =[]
        # temp:dict[tuple[int,int],dict[]] = {}

    def is_point_covered(self, x: int | float, y: int | float) -> bool:
        """
        Check if a point is covered by any rectangle.
        Returns: boolean
        """
        pass

    def find_max_overlap_point(self) -> dict:
        """
        Find a point covered by maximum number of rectangles.
        Returns: dict with 'x', 'y', 'count' keys
        Note: There might be multiple such points, return any

        one.
        """
        pass

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
        pass
