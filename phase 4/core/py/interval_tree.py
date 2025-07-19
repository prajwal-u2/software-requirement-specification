class Interval:
    """
    Represents a time interval with a start time, end time, day, and an optional game.
    This class helps to store and manage intervals, and check for overlaps with other intervals.
    """
    def __init__(self, start, end, day, week, game=None):
        """
        Initialize an interval.

        Parameters:
        - start: The start time of the interval.
        - end: The end time of the interval.
        - day: The day the interval occurs.
        - week: The week number of the year (1-52)
        - game: Optional parameter representing the game during the interval.

        Raises:
        - ValueError: If the start time is greater than the end time.
        """
        if start > end:
            raise ValueError("Start must be less than or equal to end")
        self.start = start
        self.end = end
        self.day = day
        self.game = game
        self.week = week

    def __repr__(self):
        """
        Return a string representation of the interval, including game details if available.

        If a game is associated with the interval, it will show the teams involved.
        """
        if self.game is not None:
            return f"Interval({self.start}, {self.end}) ({self.game.team1_id} vs. {self.game.team2_id})"
        else:
            return f"Interval({self.start}, {self.end})"

    def overlaps(self, other):
        """
        Check if two intervals overlap.

        Parameters:
        - other: Another Interval object to compare with.

        Returns:
        - True if the intervals overlap, False otherwise.
        """
        
        # The intervals overlap if they occur on the same day and week, and their time ranges intersect.
        return (self.day == other.day and self.week == other.week and
                self.start < other.end and other.start < self.end)


class IntervalNode:
    """
    A node in the interval tree which stores intervals and pointers to left and right children.

    Each node stores:
    - intervals: A list of intervals stored at this node.
    - max_end: The maximum end time of the intervals in the subtree rooted at this node.
    - left: A pointer to the left child node.
    - right: A pointer to the right child node.
    """
    def __init__(self, interval):
        """
        Initialize an interval node.

        Parameters:
        - interval: The interval that the node will initially hold.
        """
        self.intervals = [interval]
        self.max_end = interval.end
        self.left = None
        self.right = None


class IntervalTree:
    """
    A binary search tree for intervals. This tree allows efficient insertion of intervals and
    finding overlapping intervals using the properties of the tree.
    """
    def __init__(self):
        """Initialize an empty interval tree."""
        self.root = None

    def insert(self, interval):
        """
        Insert an interval into the tree.

        Parameters:
        - interval: The interval to insert.
        """
        if self.root is None:
            self.root = IntervalNode(interval)
        else:
            self._insert(self.root, interval)

    def _insert(self, node, interval):
        """
        Recursive helper function to insert an interval into the tree.

        Parameters:
        - node: The current node in the tree.
        - interval: The interval to insert.
        """
        # Compare the start time of the interval to decide left or right child.
        if interval.start < node.intervals[0].start:
            if node.left is None:
                node.left = IntervalNode(interval)
            else:
                self._insert(node.left, interval)
        elif interval.start > node.intervals[0].start:
            if node.right is None:
                node.right = IntervalNode(interval)
            else:
                self._insert(node.right, interval)
        else:
            # If start times are equal, add the interval to the list of intervals in the node.
            node.intervals.append(interval)

        # Update the max_end value for the node (used to prune unnecessary branches).
        node.max_end = max(node.max_end, interval.end)

    def overlap(self, interval):
        """
        Find all intervals that overlap with the given interval.

        Parameters:
        - interval: The interval to check for overlaps.

        Returns:
        - A list of overlapping intervals.
        """
        return self._overlap(self.root, interval)

    def _overlap(self, node, interval):
        """
        Recursive helper function to find all overlapping intervals in the tree.

        Parameters:
        - node: The current node in the tree.
        - interval: The interval to check for overlaps.

        Returns:
        - A list of overlapping intervals.
        """
        if node is None:
            return []

        results = []

        # Check for overlap with all intervals in the current node.
        for stored_interval in node.intervals:
            if stored_interval.overlaps(interval):
                results.append(stored_interval)

        # Recursively check the left subtree if the left child could have overlapping intervals.
        if node.left and node.left.max_end >= interval.start:
            results.extend(self._overlap(node.left, interval))

        # Recursively check the right subtree if the right child could have overlapping intervals.
        if node.right and node.intervals[0].start <= interval.end:
            results.extend(self._overlap(node.right, interval))

        return results

    def print_tree(self):
        """Print the structure of the interval tree for debugging or visualization."""
        self._print_tree(self.root, 0)

    def _print_tree(self, node, level):
        """
        Recursive helper function to print the tree.

        Parameters:
        - node: The current node to print.
        - level: The current depth in the tree (used for indentation).
        """
        if node is not None:
            self._print_tree(node.right, level + 1)
            print(' ' * 4 * level + f"{node.intervals} (Max End: {node.max_end})")
            self._print_tree(node.left, level + 1)

    def flatten(self):
        """
        Flatten the interval tree into a list of all intervals.

        Returns:
        - A list of intervals in the tree.
        """
        flattened_intervals = []
        self._flatten(self.root, flattened_intervals)
        return flattened_intervals

    def _flatten(self, node, result):
        """
        Recursive helper function to flatten the tree.

        Parameters:
        - node: The current node in the tree.
        - result: The list to store the flattened intervals.
        """
        if node is None:
            return

        # Traverse the left subtree
        self._flatten(node.left, result)

        # Add all intervals at the current node to the result
        result.extend(node.intervals)

        # Traverse the right subtree
        self._flatten(node.right, result)
