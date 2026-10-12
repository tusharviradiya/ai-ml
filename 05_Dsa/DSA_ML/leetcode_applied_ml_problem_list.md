# LeetCode Problem List: Applied ML / Product ML Engineer Interviews

A sequential, pattern-based list (fundamentals to advanced). Solve top to bottom within each section, and move to the next section when the **Must** problems feel comfortable.

**Tiers**
- **Must**: frequently tested, solve all of these first
- **Rec**: Recommended, strengthens the pattern and covers common variations
- **Adv**: Advanced, harder or less frequent, do these after Must and Rec

**Notes**
- Premium-only problems are excluded, so every link should open on a free account.
- The list is compiled from commonly tested interview patterns (heavy overlap with Blind 75 and NeetCode 150) plus extra problems that map to ML work: top-K, streaming, sampling, string similarity, graph traversal, and design problems.
- Links follow LeetCode's standard URL format. If one ever fails, search the problem number on LeetCode.
- Mark `[x]` in the Done column as you go.

---

## 1. Arrays & Hashing

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Hash map complement lookup | Must |
| [ ] | 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy | Hash set | Must |
| [ ] | 242 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Frequency count | Must |
| [ ] | 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Hash map with sorted or count key | Must |
| [ ] | 347 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Counter + heap / bucket sort | Must |
| [ ] | 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix and suffix products | Must |
| [ ] | 128 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | Hash set, sequence start | Must |
| [ ] | 169 | [Majority Element](https://leetcode.com/problems/majority-element/) | Easy | Boyer-Moore voting | Rec |
| [ ] | 283 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Easy | In-place write pointer | Rec |
| [ ] | 75 | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Medium | Dutch national flag | Rec |
| [ ] | 36 | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | Medium | Hash sets per row/col/box | Rec |
| [ ] | 692 | [Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/) | Medium | Heap with custom tie-break | Rec |
| [ ] | 41 | [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | Hard | In-place index hashing | Adv |

## 2. Prefix Sums & Matrix Basics

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 1480 | [Running Sum of 1d Array](https://leetcode.com/problems/running-sum-of-1d-array/) | Easy | Prefix sum | Rec |
| [ ] | 724 | [Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) | Easy | Prefix sum balance | Rec |
| [ ] | 303 | [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | Easy | Prefix sum array | Must |
| [ ] | 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix sum + hash map | Must |
| [ ] | 304 | [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) | Medium | 2D prefix sum | Rec |
| [ ] | 48 | [Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | Transpose + reverse | Must |
| [ ] | 54 | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Medium | Boundary simulation | Must |
| [ ] | 73 | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Medium | In-place markers | Rec |
| [ ] | 525 | [Contiguous Array](https://leetcode.com/problems/contiguous-array/) | Medium | Prefix balance + hash map | Adv |

## 3. Strings

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 125 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | Two pointers, cleaning input | Must |
| [ ] | 14 | [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | Easy | Vertical scan | Rec |
| [ ] | 8 | [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/) | Medium | Parsing and edge cases | Rec |
| [ ] | 5 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | Expand around center | Must |
| [ ] | 647 | [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | Medium | Expand around center | Rec |
| [ ] | 394 | [Decode String](https://leetcode.com/problems/decode-string/) | Medium | Stack parsing | Rec |
| [ ] | 43 | [Multiply Strings](https://leetcode.com/problems/multiply-strings/) | Medium | Digit-by-digit simulation | Adv |

## 4. Two Pointers

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 26 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Easy | Read/write pointers | Rec |
| [ ] | 88 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Easy | Merge from the back | Rec |
| [ ] | 167 | [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | Opposite-end pointers | Must |
| [ ] | 15 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | Sort + two pointers, skip duplicates | Must |
| [ ] | 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Greedy pointer move | Must |
| [ ] | 16 | [3Sum Closest](https://leetcode.com/problems/3sum-closest/) | Medium | Sort + two pointers | Rec |
| [ ] | 42 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Two pointers with max bounds | Adv |

## 5. Sliding Window

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Running min | Must |
| [ ] | 643 | [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Easy | Fixed-size window (moving average) | Rec |
| [ ] | 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Variable window + set/map | Must |
| [ ] | 424 | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | Window with max frequency | Must |
| [ ] | 567 | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Medium | Fixed window + counts | Must |
| [ ] | 438 | [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | Medium | Fixed window + counts | Rec |
| [ ] | 209 | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Variable window shrink | Rec |
| [ ] | 1004 | [Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Medium | Window with at most k flips | Rec |
| [ ] | 76 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | Window + need/have counters | Must |
| [ ] | 239 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | Monotonic deque | Adv |

## 6. Stack & Monotonic Stack

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 20 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Stack matching | Must |
| [ ] | 155 | [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Auxiliary min stack | Must |
| [ ] | 150 | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Medium | Stack evaluation | Rec |
| [ ] | 22 | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | Backtracking with counts | Must |
| [ ] | 496 | [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | Easy | Monotonic stack | Rec |
| [ ] | 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic stack | Must |
| [ ] | 503 | [Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | Medium | Circular monotonic stack | Rec |
| [ ] | 853 | [Car Fleet](https://leetcode.com/problems/car-fleet/) | Medium | Sort + stack | Rec |
| [ ] | 84 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Monotonic stack | Adv |

## 7. Binary Search

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 704 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | Classic template | Must |
| [ ] | 278 | [First Bad Version](https://leetcode.com/problems/first-bad-version/) | Easy | Search for boundary | Rec |
| [ ] | 69 | [Sqrt(x)](https://leetcode.com/problems/sqrtx/) | Easy | Binary search on answer | Rec |
| [ ] | 74 | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | Medium | Flatten index mapping | Must |
| [ ] | 34 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Medium | Lower/upper bound | Must |
| [ ] | 153 | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Medium | Rotated array search | Must |
| [ ] | 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Rotated array search | Must |
| [ ] | 162 | [Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Medium | Binary search on slope | Rec |
| [ ] | 875 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | Binary search on answer | Must |
| [ ] | 1011 | [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | Binary search on answer | Rec |
| [ ] | 981 | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Medium | Hash map + binary search | Must |
| [ ] | 4 | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | Partition binary search | Adv |

## 8. Linked List

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Iterative pointer reversal | Must |
| [ ] | 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Dummy node merge | Must |
| [ ] | 141 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Fast/slow pointers | Must |
| [ ] | 876 | [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Easy | Fast/slow pointers | Rec |
| [ ] | 19 | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Gap two pointers | Must |
| [ ] | 143 | [Reorder List](https://leetcode.com/problems/reorder-list/) | Medium | Middle + reverse + merge | Rec |
| [ ] | 2 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | Carry simulation | Rec |
| [ ] | 142 | [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | Medium | Floyd cycle start | Rec |
| [ ] | 138 | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | Hash map clone | Rec |
| [ ] | 23 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | Min-heap k-way merge | Must |
| [ ] | 25 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Hard | Group reversal | Adv |

## 9. Trees (Binary Trees & BST)

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 104 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | DFS recursion | Must |
| [ ] | 226 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | DFS recursion | Must |
| [ ] | 100 | [Same Tree](https://leetcode.com/problems/same-tree/) | Easy | Parallel DFS | Must |
| [ ] | 572 | [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | Easy | DFS + same-tree check | Rec |
| [ ] | 543 | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | DFS returning height | Must |
| [ ] | 110 | [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | Easy | DFS returning height | Rec |
| [ ] | 102 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | BFS with queue | Must |
| [ ] | 199 | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | Medium | BFS by level | Rec |
| [ ] | 235 | [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Medium | BST property | Must |
| [ ] | 236 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | Post-order DFS | Must |
| [ ] | 98 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | DFS with bounds | Must |
| [ ] | 230 | [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Medium | Inorder traversal | Must |
| [ ] | 1448 | [Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | Medium | DFS carrying max | Rec |
| [ ] | 105 | [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Medium | Recursion + index map | Rec |
| [ ] | 124 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | DFS with global max | Adv |
| [ ] | 297 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | Preorder / BFS encoding | Adv |

## 10. Tries

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 208 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Trie node dict | Must |
| [ ] | 211 | [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | Trie + DFS wildcard | Rec |
| [ ] | 212 | [Word Search II](https://leetcode.com/problems/word-search-ii/) | Hard | Trie + backtracking | Adv |

## 11. Heap / Priority Queue & Top-K

Top-K, streaming, and ranking problems are especially relevant to ML roles (retrieval, recommendations, nearest neighbors).

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 703 | [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Easy | Min-heap of size k | Must |
| [ ] | 1046 | [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | Easy | Max-heap simulation | Rec |
| [ ] | 973 | [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Heap / quickselect (kNN flavor) | Must |
| [ ] | 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Heap or quickselect | Must |
| [ ] | 621 | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Medium | Greedy + heap / formula | Rec |
| [ ] | 373 | [Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) | Medium | Heap expansion | Rec |
| [ ] | 355 | [Design Twitter](https://leetcode.com/problems/design-twitter/) | Medium | Merge k feeds with heap | Must |
| [ ] | 295 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | Two heaps | Must |
| [ ] | 502 | [IPO](https://leetcode.com/problems/ipo/) | Hard | Greedy + two heaps | Adv |

## 12. Intervals

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 56 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Sort by start | Must |
| [ ] | 57 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Medium | Linear merge | Must |
| [ ] | 435 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | Greedy by end | Rec |
| [ ] | 986 | [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | Medium | Two pointers | Rec |
| [ ] | 2406 | [Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/) | Medium | Sweep line / heap | Adv |

## 13. Greedy

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | Kadane's algorithm | Must |
| [ ] | 55 | [Jump Game](https://leetcode.com/problems/jump-game/) | Medium | Farthest reach | Must |
| [ ] | 45 | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Medium | Greedy BFS layers | Rec |
| [ ] | 134 | [Gas Station](https://leetcode.com/problems/gas-station/) | Medium | Running surplus | Rec |
| [ ] | 763 | [Partition Labels](https://leetcode.com/problems/partition-labels/) | Medium | Last occurrence greedy | Rec |
| [ ] | 846 | [Hand of Straights](https://leetcode.com/problems/hand-of-straights/) | Medium | Greedy + counter | Adv |

## 14. Backtracking

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 78 | [Subsets](https://leetcode.com/problems/subsets/) | Medium | Include/exclude recursion | Must |
| [ ] | 46 | [Permutations](https://leetcode.com/problems/permutations/) | Medium | Used array backtracking | Must |
| [ ] | 39 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Medium | Reuse elements | Must |
| [ ] | 90 | [Subsets II](https://leetcode.com/problems/subsets-ii/) | Medium | Sort + skip duplicates | Rec |
| [ ] | 40 | [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | Medium | Sort + skip duplicates | Rec |
| [ ] | 79 | [Word Search](https://leetcode.com/problems/word-search/) | Medium | Grid DFS backtracking | Must |
| [ ] | 131 | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | Medium | Partition backtracking | Rec |
| [ ] | 17 | [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Medium | Cartesian product backtracking | Rec |
| [ ] | 51 | [N-Queens](https://leetcode.com/problems/n-queens/) | Hard | Constraint backtracking | Adv |

## 15. Graphs (DFS, BFS, Topological Sort, Shortest Path)

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Grid DFS/BFS | Must |
| [ ] | 695 | [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | Medium | Grid DFS | Must |
| [ ] | 133 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | Medium | DFS + hash map | Must |
| [ ] | 994 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | Multi-source BFS | Must |
| [ ] | 542 | [01 Matrix](https://leetcode.com/problems/01-matrix/) | Medium | Multi-source BFS | Rec |
| [ ] | 417 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Reverse DFS from borders | Rec |
| [ ] | 130 | [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | Medium | Border DFS | Rec |
| [ ] | 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Cycle detection / topo sort | Must |
| [ ] | 210 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Medium | Kahn's topological sort | Must |
| [ ] | 785 | [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | Medium | BFS coloring | Rec |
| [ ] | 743 | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Medium | Dijkstra | Must |
| [ ] | 787 | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Medium | Bellman-Ford / BFS levels | Rec |
| [ ] | 1631 | [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | Medium | Dijkstra on grid | Adv |
| [ ] | 127 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | BFS on implicit graph | Adv |
| [ ] | 332 | [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) | Hard | Eulerian path (Hierholzer) | Adv |

## 16. Union-Find

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 547 | [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Medium | Union-Find or DFS | Must |
| [ ] | 684 | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Medium | Union-Find cycle detection | Must |
| [ ] | 721 | [Accounts Merge](https://leetcode.com/problems/accounts-merge/) | Medium | Union-Find on strings (entity resolution flavor) | Rec |
| [ ] | 1202 | [Smallest String With Swaps](https://leetcode.com/problems/smallest-string-with-swaps/) | Medium | Union-Find + sorting | Adv |

## 17. Dynamic Programming: 1D

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | Fibonacci recurrence | Must |
| [ ] | 746 | [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | Easy | 1D DP | Rec |
| [ ] | 198 | [House Robber](https://leetcode.com/problems/house-robber/) | Medium | Take/skip DP | Must |
| [ ] | 213 | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | Medium | Circular DP | Rec |
| [ ] | 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Unbounded knapsack | Must |
| [ ] | 300 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | Medium | DP O(n^2) and binary search O(n log n) | Must |
| [ ] | 139 | [Word Break](https://leetcode.com/problems/word-break/) | Medium | String DP | Must |
| [ ] | 152 | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Medium | Track min and max | Rec |
| [ ] | 91 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | Medium | Counting DP | Rec |
| [ ] | 416 | [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Medium | 0/1 knapsack | Must |
| [ ] | 377 | [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) | Medium | Ordered counting DP | Adv |

## 18. Dynamic Programming: 2D / Strings

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 62 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | Medium | Grid DP | Must |
| [ ] | 64 | [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | Medium | Grid DP | Rec |
| [ ] | 1143 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Medium | 2D string DP | Must |
| [ ] | 72 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Medium | 2D string DP (string similarity, NLP flavor) | Must |
| [ ] | 518 | [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Medium | Unbounded knapsack counting | Rec |
| [ ] | 494 | [Target Sum](https://leetcode.com/problems/target-sum/) | Medium | Subset-sum transformation | Rec |
| [ ] | 97 | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | Medium | 2D DP | Adv |
| [ ] | 115 | [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | Hard | 2D counting DP | Adv |
| [ ] | 10 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard | 2D DP with wildcards | Adv |
| [ ] | 312 | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Hard | Interval DP | Adv |

## 19. Design Problems (Data Structure Design)

These are common in product-company rounds and map well to real ML serving systems (caching, sampling, rate limiting).

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 146 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Hash map + doubly linked list / OrderedDict | Must |
| [ ] | 380 | [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | Medium | Hash map + array swap-delete | Must |
| [ ] | 981 | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Medium | Covered in Binary Search section | Must |
| [ ] | 355 | [Design Twitter](https://leetcode.com/problems/design-twitter/) | Medium | Covered in Heap section | Must |
| [ ] | 362 | [Design Hit Counter](https://leetcode.com/problems/design-hit-counter/) | Medium | Premium problem, skip if no access | Rec |
| [ ] | 460 | [LFU Cache](https://leetcode.com/problems/lfu-cache/) | Hard | Frequency buckets + linked lists | Adv |

> Note: #981 and #355 repeat from earlier sections, so solve them only once. #362 requires LeetCode Premium. Skip it if you do not have access.

## 20. Sampling, Probability & Math (ML-Flavored)

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 384 | [Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) | Medium | Fisher-Yates shuffle | Must |
| [ ] | 528 | [Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) | Medium | Prefix sum + binary search (weighted sampling) | Must |
| [ ] | 398 | [Random Pick Index](https://leetcode.com/problems/random-pick-index/) | Medium | Reservoir sampling | Rec |
| [ ] | 50 | [Pow(x, n)](https://leetcode.com/problems/powx-n/) | Medium | Fast exponentiation | Rec |
| [ ] | 66 | [Plus One](https://leetcode.com/problems/plus-one/) | Easy | Carry handling | Rec |
| [ ] | 912 | [Sort an Array](https://leetcode.com/problems/sort-an-array/) | Medium | Implement merge sort / quick sort | Rec |

## 21. Bit Manipulation (Light Coverage)

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 136 | [Single Number](https://leetcode.com/problems/single-number/) | Easy | XOR | Rec |
| [ ] | 191 | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Easy | Bit counting | Rec |
| [ ] | 338 | [Counting Bits](https://leetcode.com/problems/counting-bits/) | Easy | DP with bits | Rec |
| [ ] | 268 | [Missing Number](https://leetcode.com/problems/missing-number/) | Easy | XOR / sum formula | Rec |

---

## Python Tips for These Problems

- Know these well: `collections.Counter`, `defaultdict`, `deque`, `OrderedDict`, `heapq` (min-heap only, negate values for max-heap), `bisect_left` / `bisect_right`, `itertools` (`combinations`, `permutations`), and `functools.lru_cache` for memoization.
- Use `heapq.nlargest` and `heapq.nsmallest` for quick Top-K, but be ready to implement the heap approach by hand.
- Python's recursion limit is about 1000. For deep DFS, mention converting to an iterative version.
- Practice stating time and space complexity for every solution out loud. This matters as much as the code.
- Always handle empty input, single element, duplicates, and negative numbers.

## How to Use This List

1. Within each section, do **Must** problems first, then **Rec**, then **Adv**.
2. For each problem: try for 20-25 minutes, then read the solution, then re-solve it from scratch a few days later.
3. Keep a mistakes log with the pattern you missed. Review it weekly.
4. Do not grind all **Adv** problems. Attempt them once Must and Rec feel comfortable.
5. Once comfortable, do mixed timed sets (2 mediums in 45 minutes) to simulate real interviews.

## Count Summary (approximate)

| Tier | Approx. Count |
|---|---|
| Must | ~85 |
| Rec | ~75 |
| Adv | ~25 |
