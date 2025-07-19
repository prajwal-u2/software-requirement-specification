import java.util.ArrayList;
import java.util.List;

/**
 * Represents an interval of time with a start and end time, along with an
 * optional associated game.
 */
class Interval {
    double start;
    double end;
    int day;
    Game game;

    /**
     * Initialize an Interval object.
     * 
     * @param start The start time of the interval.
     * @param end   The end time of the interval.
     * @param day   The day the interval occurs.
     * @param week  The week number of the year (1-52)
     * @param game  Optional parameter representing the game associated with the
     *              interval.
     */
    public Interval(double start, double end, int day, int week, Game game) {
        if (start > end) {
            throw new IllegalArgumentException("Start must be less than or equal to end");
        }
        this.start = start;
        this.end = end;
        this.day = day;
        this.game = game;
        this.week = week;
    }

    /**
     * Returns a string representation of the interval.
     * 
     * @return A string representation of the interval.
     */
    public String repr() {
        if (game != null) {
            return "Interval(" + start + ", " + end + ") (" + game.team1_id + " vs. " + game.team2_id + ")";
        }
        return "Interval(" + start + ", " + end + ")";
    }

    /**
     * Checks if this interval overlaps with another interval.
     * 
     * @param other The other interval to check for overlap.
     * @return True if the intervals overlap, otherwise false.
     */
    public boolean overlaps(Interval other) {
        // Intervals overlap if they are on the same day and week, and their time ranges
        // intersect.
        return this.day == other.day && this.week == other.week && start < other.end && other.start < end;
    }
}

/**
 * Represents a node in the interval tree, containing a list of intervals and
 * pointers to left and right subtrees.
 */
class IntervalNode {
    List<Interval> intervals;
    double max_end;
    IntervalNode left;
    IntervalNode right;

    /**
     * Initializes an interval node with a given interval.
     * 
     * @param interval The interval to store in this node.
     */
    public IntervalNode(Interval interval) {
        this.intervals = new ArrayList<>();
        this.intervals.add(interval);
        this.max_end = interval.end;
        this.left = null;
        this.right = null;
    }
}

/**
 * Represents an interval tree, providing methods to insert intervals and find
 * overlapping intervals.
 */
class IntervalTree {
    IntervalNode root;

    /**
     * Initializes an empty interval tree.
     */
    public IntervalTree() {
        this.root = null;
    }

    /**
     * Inserts an interval into the tree.
     * 
     * @param interval The interval to insert into the tree.
     */
    public void insert(Interval interval) {
        if (root == null) {
            root = new IntervalNode(interval);
        } else {
            insert(root, interval);
        }
    }

    /**
     * Recursive helper function to insert an interval into the tree.
     * 
     * @param node     The current node.
     * @param interval The interval to insert.
     */
    private void insert(IntervalNode node, Interval interval) {
        if (interval.start < node.intervals.get(0).start) {
            if (node.left == null) {
                node.left = new IntervalNode(interval);
            } else {
                insert(node.left, interval);
            }
        } else if (interval.start > node.intervals.get(0).start) {
            if (node.right == null) {
                node.right = new IntervalNode(interval);
            } else {
                insert(node.right, interval);
            }
        } else {
            // If the start is the same, add to the list of intervals.
            node.intervals.add(interval);
        }

        // Update the max_end of the current node.
        node.max_end = Math.max(node.max_end, interval.end);
    }

    /**
     * Finds all intervals that overlap with the given interval.
     * 
     * @param interval The interval to check for overlaps.
     * @return A list of overlapping intervals.
     */
    public List<Interval> overlap(Interval interval) {
        return overlap(root, interval);
    }

    /**
     * Recursive helper function to find overlapping intervals.
     * 
     * @param node     The current node in the tree.
     * @param interval The interval to check for overlaps.
     * @return A list of overlapping intervals.
     */
    private List<Interval> overlap(IntervalNode node, Interval interval) {
        List<Interval> results = new ArrayList<>();

        if (node == null) {
            return results;
        }

        // Check for overlap with all intervals at the current node.
        for (Interval storedInterval : node.intervals) {
            if (storedInterval.overlaps(interval)) {
                results.add(storedInterval);
            }
        }

        // Recursively check the left subtree if it could have overlapping intervals.
        if (node.left != null && node.left.max_end >= interval.start) {
            results.addAll(overlap(node.left, interval));
        }

        // Recursively check the right subtree if it could have overlapping intervals.
        if (node.right != null && node.intervals.get(0).start <= interval.end) {
            results.addAll(overlap(node.right, interval));
        }

        return results;
    }

    /**
     * Prints the tree structure for debugging purposes.
     */
    public void printTree() {
        printTree(root, 0);
    }

    /**
     * Recursive helper function to print the tree structure.
     * 
     * @param node  The current node.
     * @param level The current level in the tree (used for indentation).
     */
    private void printTree(IntervalNode node, int level) {
        if (node == null) {
            return;
        }

        printTree(node.right, level + 1);
        System.out.println(" ".repeat(level * 4) + node.intervals + " (Max End: " + node.max_end + ")");
        printTree(node.left, level + 1);
    }

    /**
     * Flattens the interval tree into a list of all intervals.
     * 
     * @return A list of all intervals in the tree.
     */
    public List<Interval> flatten() {
        List<Interval> flattenedIntervals = new ArrayList<>();
        flatten(root, flattenedIntervals);
        return flattenedIntervals;
    }

    /**
     * Recursive helper function to flatten the tree.
     * 
     * @param node   The current node.
     * @param result The list to store the flattened intervals.
     */
    private void flatten(IntervalNode node, List<Interval> result) {
        if (node == null) {
            return;
        }

        // Traverse left subtree
        flatten(node.left, result);

        // Add all intervals at the current node to the result
        result.addAll(node.intervals);

        // Traverse right subtree
        flatten(node.right, result);
    }
}