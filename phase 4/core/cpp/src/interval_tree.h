#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>

class Interval {
public:
    double start;
    double end;
    int day;
    Game* game;

    /**
     * Initialize an interval.
     * 
     * @param start The start time of the interval.
     * @param end The end time of the interval.
     * @param day The day the interval occurs.
     * @param week: The week number of the year (1-52)
     * @param game Optional parameter representing the game during the interval.
     */
    Interval(double start, double end, int day, int week, Game* game = nullptr)
        : start(start), end(end), day(day), game(game) {
        if (start > end) {
            throw std::invalid_argument("Start must be less than or equal to end");
        }
    }

    /**
     * Print the interval details.
     */
    std::string repr() const {
        if (game != nullptr) {
            return "Interval(" + std::to_string(start) + ", " + std::to_string(end) + ") (" + 
                   std::to_string(game->team1_id) + " vs. " + std::to_string(game->team2_id) + ")";
        }
        return "Interval(" + std::to_string(start) + ", " + std::to_string(end) + ")";
    }

    /**
     * Check if two intervals overlap.
     * 
     * @param other Another interval to compare with.
     * @return True if intervals overlap, False otherwise.
     */
    bool overlaps(const Interval& other) const {
        // Intervals overlap if they are on the same day and week, and time ranges intersect.
        return (this->day == other.day && this->week == other.week && 
                start < other.end && other.start < end);
    }
};

class IntervalNode {
public:
    std::vector<Interval> intervals;
    double max_end;
    IntervalNode* left;
    IntervalNode* right;

    /**
     * Initialize an interval node.
     * 
     * @param interval The interval to store in this node.
     */
    IntervalNode(const Interval& interval) 
        : intervals{interval}, max_end(interval.end), left(nullptr), right(nullptr) {}
};

class IntervalTree {
public:
    IntervalNode* root;

    /**
     * Initialize the interval tree with no root.
     */
    IntervalTree() : root(nullptr) {}

    /**
     * Insert an interval into the tree.
     * 
     * @param interval The interval to insert.
     */
    void insert(const Interval& interval) {
        if (root == nullptr) {
            root = new IntervalNode(interval);
        } else {
            insert(root, interval);
        }
    }

private:
    /**
     * Recursive helper function to insert an interval into the tree.
     * 
     * @param node The current node in the tree.
     * @param interval The interval to insert.
     */
    void insert(IntervalNode* node, const Interval& interval) {
        if (interval.start < node->intervals[0].start) {
            if (node->left == nullptr) {
                node->left = new IntervalNode(interval);
            } else {
                insert(node->left, interval);
            }
        } else if (interval.start > node->intervals[0].start) {
            if (node->right == nullptr) {
                node->right = new IntervalNode(interval);
            } else {
                insert(node->right, interval);
            }
        } else {
            // If the start is the same, add to the list of intervals.
            node->intervals.push_back(interval);
        }

        // Update the max_end of the current node.
        node->max_end = std::max(node->max_end, interval.end);
    }

public:
    /**
     * Find all intervals that overlap with the given interval.
     * 
     * @param interval The interval to check for overlaps.
     * @return A list of overlapping intervals.
     */
    std::vector<Interval> overlap(const Interval& interval) {
        return overlap(root, interval);
    }

private:
    /**
     * Recursive helper function to find overlapping intervals.
     * 
     * @param node The current node in the tree.
     * @param interval The interval to check for overlaps.
     * @return A list of overlapping intervals.
     */
    std::vector<Interval> overlap(IntervalNode* node, const Interval& interval) {
        std::vector<Interval> results;

        if (node == nullptr) {
            return results;
        }

        // Check for overlap with all intervals in the current node.
        for (const auto& stored_interval : node->intervals) {
            if (stored_interval.overlaps(interval)) {
                results.push_back(stored_interval);
            }
        }

        // Recursively check the left subtree if the left child could have overlapping intervals.
        if (node->left != nullptr && node->left->max_end >= interval.start) {
            auto left_results = overlap(node->left, interval);
            results.insert(results.end(), left_results.begin(), left_results.end());
        }

        // Recursively check the right subtree if the right child could have overlapping intervals.
        if (node->right != nullptr && node->intervals[0].start <= interval.end) {
            auto right_results = overlap(node->right, interval);
            results.insert(results.end(), right_results.begin(), right_results.end());
        }

        return results;
    }

public:
    /**
     * Print the structure of the interval tree for debugging or visualization.
     */
    void print_tree() {
        print_tree(root, 0);
    }

private:
    /**
     * Recursive helper function to print the tree.
     * 
     * @param node The current node in the tree.
     * @param level The current depth in the tree (used for indentation).
     */
    void print_tree(IntervalNode* node, int level) {
        if (node == nullptr) {
            return;
        }
        print_tree(node->right, level + 1);
        std::cout << std::string(level * 4, ' ') << "[" << node->intervals.size() << "] (Max End: " << node->max_end << ")\n";
        print_tree(node->left, level + 1);
    }

public:
    /**
     * Flatten the interval tree into a list of all intervals.
     * 
     * @return A list of intervals in the tree.
     */
    std::vector<Interval> flatten() {
        std::vector<Interval> flattened_intervals;
        flatten(root, flattened_intervals);
        return flattened_intervals;
    }

private:
    /**
     * Recursive helper function to flatten the tree.
     * 
     * @param node The current node in the tree.
     * @param result The list to store the flattened intervals.
     */
    void flatten(IntervalNode* node, std::vector<Interval>& result) {
        if (node == nullptr) {
            return;
        }

        // Traverse left subtree
        flatten(node->left, result);

        // Add all intervals at the current node to the result
        result.insert(result.end(), node->intervals.begin(), node->intervals.end());

        // Traverse right subtree
        flatten(node->right, result);
    }
};

int main() {
    // Example usage
    Game game1(1, 2, 1, 1);
    Game game2(3, 4, 1, 1);

    Interval interval1(1.0, 3.0, 1, &game1);
    Interval interval2(2.0, 4.0, 1, &game2);

    IntervalTree tree;
    tree.insert(interval1);
    tree.insert(interval2);

    // Check overlap
    auto overlaps = tree.overlap(interval1);
    for (const auto& overlap : overlaps) {
        std::cout << overlap.repr() << "\n";
    }

    return 0;
}
