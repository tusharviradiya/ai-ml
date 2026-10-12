# LeetCode Roadmap for Applied ML / Product ML Engineer Interviews

A sequenced list of **136 problems** for the coding rounds of Applied ML and Product ML Engineer interviews. It runs from fundamentals to advanced patterns, is weighted toward the Easy and Medium problems that these loops lean on, and includes extra problems that map to ML work: top-K, streaming, sampling, string similarity, entity resolution, and caching.

It was produced by merging two lists (a 66-problem list and a 180-problem list), removing duplicates, cutting near-repeats, and re-sequencing. See [How this list was built](#how-this-list-was-built).

## Contents

- [At a glance](#at-a-glance)
- [How to use this list](#how-to-use-this-list)
- [Pacing](#pacing)
- [Python toolkit](#python-toolkit)
- [The problem list](#the-problem-list)
- [Beyond LeetCode: ML-flavored coding practice](#beyond-leetcode-ml-flavored-coding-practice)
- [How this list was built](#how-this-list-was-built)

---

## At a glance

| Tier | Meaning | Count |
|---|---|---|
| **Must** | High-frequency patterns. Solve all of these. | 73 |
| Rec | Recommended. Reinforces a pattern or covers a common variation. | 53 |
| Adv | Advanced. Harder or less frequent. Do these last. | 10 |
| **Total** | 27 Easy, 97 Medium, 12 Hard | **136** |

| # | Section | Problems | Must | Rec | Adv |
|---|---|---|---|---|---|
| 1 | Arrays & Hashing | 10 | 5 | 5 | 0 |
| 2 | Prefix Sums, Kadane & Matrix | 7 | 5 | 2 | 0 |
| 3 | Strings | 4 | 2 | 2 | 0 |
| 4 | Two Pointers | 5 | 3 | 1 | 1 |
| 5 | Sliding Window | 8 | 4 | 3 | 1 |
| 6 | Stack & Monotonic Stack | 6 | 3 | 2 | 1 |
| 7 | Binary Search | 11 | 7 | 3 | 1 |
| 8 | Linked List | 8 | 5 | 3 | 0 |
| 9 | Trees (Binary Trees & BST) | 13 | 6 | 5 | 2 |
| 10 | Tries | 3 | 1 | 1 | 1 |
| 11 | Heaps & Top-K | 8 | 5 | 3 | 0 |
| 12 | Intervals | 5 | 2 | 3 | 0 |
| 13 | Greedy | 4 | 1 | 3 | 0 |
| 14 | Backtracking | 8 | 5 | 3 | 0 |
| 15 | Graphs (DFS, BFS, Topological Sort, Shortest Path) | 10 | 5 | 3 | 2 |
| 16 | Union-Find | 3 | 2 | 1 | 0 |
| 17 | Dynamic Programming: 1D | 9 | 6 | 3 | 0 |
| 18 | Dynamic Programming: 2D & Strings | 4 | 3 | 1 | 0 |
| 19 | Design, Sampling & Math (ML-Flavored) | 7 | 3 | 3 | 1 |
| 20 | Bit Manipulation (Light Coverage) | 3 | 0 | 3 | 0 |

---

## How to use this list

1. **Go section by section, top to bottom.** Within each section the order is a difficulty ramp, so easier problems come first even if their tier is Rec. Do not jump around.
2. **If time is short, skip by tier.** Drop Adv first, then Rec. The Must problems alone still cover every core pattern.
3. **Save Adv problems for a final pass** after you have finished the Must and Rec problems in all sections.
4. **Time-box each attempt to 20 to 25 minutes.** If you are stuck, read the solution, then close it and re-solve from scratch.
5. **Re-solve Must problems 2 to 3 days later, and again a week later**, without notes. Spaced repetition beats solving more problems.
6. **Keep a mistakes log** with the pattern you missed and why. Review it weekly.
7. **State time and space complexity out loud** for every solution. Interviewers weigh this as much as the code.
8. **Handle edge cases deliberately:** empty input, a single element, duplicates, and negative numbers.
9. **Once you finish a few sections, practice mixed timed sets**, for example 2 Mediums in 45 minutes, to simulate a real round.

Tick the **Done** column as you go. Replace `[ ]` with `[x]`.

---

## Pacing

Rough timelines, assuming you solve problems and review the earlier ones on the same schedule:

| Track | Problems | At ~10 per week | At ~20 per week |
|---|---|---|---|
| Must only | 73 | ~8 weeks | ~4 weeks |
| Must + Rec | 126 | ~13 weeks | ~7 weeks |
| Everything | 136 | ~14 weeks | ~7 weeks |

DSA is usually one part of an Applied ML loop, alongside ML fundamentals, ML system design, and behavioral rounds. Do not let this list crowd out the rest of your preparation.

---

## Python toolkit

Know these cold. Interviewers notice fluent use of the standard library.

```python
import heapq, bisect
from collections import Counter, defaultdict, deque, OrderedDict
from functools import lru_cache

# Heaps: heapq is a min-heap, so negate values for a max-heap
h = []
heapq.heappush(h, -x)
largest = -heapq.heappop(h)
heapq.nlargest(k, nums)                 # quick top-k; be ready to write the heap version by hand
heapq.nsmallest(k, items, key=lambda p: p[0])

# Binary search
i = bisect.bisect_left(a, x)             # first index with a[i] >= x
j = bisect.bisect_right(a, x)            # first index with a[j] > x

# Counting and grouping
cnt = Counter(s)
groups = defaultdict(list)
q = deque()                              # O(1) pops from both ends (BFS, monotonic deque)

# Memoization
@lru_cache(maxsize=None)
def dp(i):
    ...
```

- `OrderedDict` with `move_to_end` makes a compact LRU Cache, but be ready to build the hash map + doubly linked list version too.
- Python's default recursion limit is about 1000. For deep DFS, mention that you would convert to an iterative version.
- `itertools.combinations` and `permutations` are fine for checking your work, but write the backtracking by hand in the interview.

---

## The problem list

All links use LeetCode's standard URL format. If one fails, search for the problem number on LeetCode.

### 1. Arrays & Hashing

Hash map and hash set fluency. Almost every later pattern builds on this.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy | Hash set | Rec |
| [ ] | 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Hash map complement lookup | **Must** |
| [ ] | 242 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Frequency count | Rec |
| [ ] | 49 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Hash map with sorted or count key | **Must** |
| [ ] | 347 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Counter + heap / bucket sort | **Must** |
| [ ] | 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix and suffix products | **Must** |
| [ ] | 128 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | Hash set, sequence start | **Must** |
| [ ] | 169 | [Majority Element](https://leetcode.com/problems/majority-element/) | Easy | Boyer-Moore voting | Rec |
| [ ] | 283 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Easy | In-place write pointer | Rec |
| [ ] | 75 | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Medium | Dutch national flag | Rec |

### 2. Prefix Sums, Kadane & Matrix

Running aggregates and in-place matrix work, which show up constantly in data-processing style questions.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | Kadane's algorithm | **Must** |
| [ ] | 303 | [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | Easy | Prefix sum array | **Must** |
| [ ] | 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix sum + hash map | **Must** |
| [ ] | 304 | [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) | Medium | 2D prefix sum | Rec |
| [ ] | 48 | [Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | Transpose + reverse | **Must** |
| [ ] | 54 | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Medium | Boundary simulation | **Must** |
| [ ] | 73 | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Medium | In-place markers | Rec |

### 3. Strings

Parsing, cleaning input, and edge cases. More string work appears in Sliding Window, Stack, and DP.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 125 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | Two pointers, cleaning input | **Must** |
| [ ] | 14 | [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | Easy | Vertical scan | Rec |
| [ ] | 8 | [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/) | Medium | Parsing and edge cases | Rec |
| [ ] | 5 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | Expand around center | **Must** |

### 4. Two Pointers

Opposite-end and read/write pointers, plus the sort-then-scan pattern.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 88 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Easy | Merge from the back | Rec |
| [ ] | 167 | [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | Opposite-end pointers | **Must** |
| [ ] | 15 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | Sort + two pointers, skip duplicates | **Must** |
| [ ] | 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Greedy pointer move | **Must** |
| [ ] | 42 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Two pointers with max bounds | Adv |

### 5. Sliding Window

Rolling-window logic, the same idea behind streaming metrics and moving averages.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Running min | **Must** |
| [ ] | 643 | [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Easy | Fixed-size window (moving average) | Rec |
| [ ] | 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Variable window + set/map | **Must** |
| [ ] | 424 | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | Window with max frequency | **Must** |
| [ ] | 567 | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Medium | Fixed window + counts | **Must** |
| [ ] | 209 | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Variable window shrink | Rec |
| [ ] | 76 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | Window + need/have counters | Rec |
| [ ] | 239 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | Monotonic deque | Adv |

### 6. Stack & Monotonic Stack

Matching, parsing, and next-greater-element patterns.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 20 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Stack matching | **Must** |
| [ ] | 155 | [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Auxiliary min stack | **Must** |
| [ ] | 150 | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Medium | Stack evaluation | Rec |
| [ ] | 739 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic stack | **Must** |
| [ ] | 394 | [Decode String](https://leetcode.com/problems/decode-string/) | Medium | Stack parsing | Rec |
| [ ] | 84 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Monotonic stack | Adv |

### 7. Binary Search

Includes binary search on the answer and time-based lookups (feature-store flavor).

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 704 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | Classic template | **Must** |
| [ ] | 278 | [First Bad Version](https://leetcode.com/problems/first-bad-version/) | Easy | Search for boundary | Rec |
| [ ] | 69 | [Sqrt(x)](https://leetcode.com/problems/sqrtx/) | Easy | Binary search on answer | Rec |
| [ ] | 74 | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | Medium | Flatten index mapping | **Must** |
| [ ] | 34 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Medium | Lower/upper bound | **Must** |
| [ ] | 153 | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Medium | Rotated array search | **Must** |
| [ ] | 33 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Rotated array search | **Must** |
| [ ] | 162 | [Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Medium | Binary search on slope | Rec |
| [ ] | 875 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | Binary search on answer | **Must** |
| [ ] | 981 | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Medium | Hash map + binary search | **Must** |
| [ ] | 4 | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | Partition binary search | Adv |

### 8. Linked List

Pointer manipulation, ending with LRU Cache, which combines a hash map with a doubly linked list.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Iterative pointer reversal | **Must** |
| [ ] | 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Dummy node merge | **Must** |
| [ ] | 141 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Fast/slow pointers | **Must** |
| [ ] | 142 | [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | Medium | Floyd cycle start | Rec |
| [ ] | 19 | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Gap two pointers | **Must** |
| [ ] | 2 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | Carry simulation | Rec |
| [ ] | 143 | [Reorder List](https://leetcode.com/problems/reorder-list/) | Medium | Middle + reverse + merge | Rec |
| [ ] | 146 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Hash map + doubly linked list / OrderedDict | **Must** |

### 9. Trees (Binary Trees & BST)

Recursion on trees, BFS by level, and BST properties. Do the Easy ones quickly and spend your time on the Mediums.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 104 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | DFS recursion | **Must** |
| [ ] | 226 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | DFS recursion | Rec |
| [ ] | 100 | [Same Tree](https://leetcode.com/problems/same-tree/) | Easy | Parallel DFS | Rec |
| [ ] | 543 | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | DFS returning height | **Must** |
| [ ] | 102 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | BFS with queue | **Must** |
| [ ] | 199 | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | Medium | BFS by level | Rec |
| [ ] | 98 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | DFS with bounds | **Must** |
| [ ] | 230 | [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Medium | Inorder traversal | **Must** |
| [ ] | 235 | [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Medium | BST property | Rec |
| [ ] | 236 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | Post-order DFS | **Must** |
| [ ] | 105 | [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Medium | Recursion + index map | Rec |
| [ ] | 124 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | DFS with global max | Adv |
| [ ] | 297 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | Preorder / BFS encoding | Adv |

### 10. Tries

Prefix search, the data structure behind autocomplete.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 208 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Trie node dict | **Must** |
| [ ] | 211 | [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | Trie + DFS wildcard | Rec |
| [ ] | 212 | [Word Search II](https://leetcode.com/problems/word-search-ii/) | Hard | Trie + backtracking | Adv |

### 11. Heaps & Top-K

Top-K, streaming, and ranking problems map directly to retrieval, recommendation, and nearest-neighbor work.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 703 | [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Easy | Min-heap of size k | **Must** |
| [ ] | 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Heap or quickselect | **Must** |
| [ ] | 973 | [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Heap / quickselect (kNN flavor) | **Must** |
| [ ] | 692 | [Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/) | Medium | Heap with custom tie-break | Rec |
| [ ] | 621 | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Medium | Greedy + heap / formula | Rec |
| [ ] | 23 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | Min-heap k-way merge | **Must** |
| [ ] | 355 | [Design Twitter](https://leetcode.com/problems/design-twitter/) | Medium | Merge k feeds with heap | Rec |
| [ ] | 295 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | Two heaps | **Must** |

### 12. Intervals

Sorting plus sweeping. #2406 is the free equivalent of the premium Meeting Rooms II.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 56 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Sort by start | **Must** |
| [ ] | 57 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Medium | Linear merge | **Must** |
| [ ] | 435 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | Greedy by end | Rec |
| [ ] | 986 | [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | Medium | Two pointers | Rec |
| [ ] | 2406 | [Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/) | Medium | Sweep line / heap | Rec |

### 13. Greedy

Local choices that provably give a global optimum. Kadane's algorithm (#53) lives in section 2.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 55 | [Jump Game](https://leetcode.com/problems/jump-game/) | Medium | Farthest reach | **Must** |
| [ ] | 45 | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Medium | Greedy BFS layers | Rec |
| [ ] | 134 | [Gas Station](https://leetcode.com/problems/gas-station/) | Medium | Running surplus | Rec |
| [ ] | 763 | [Partition Labels](https://leetcode.com/problems/partition-labels/) | Medium | Last occurrence greedy | Rec |

### 14. Backtracking

Include/exclude recursion, pruning, and duplicate handling.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 78 | [Subsets](https://leetcode.com/problems/subsets/) | Medium | Include/exclude recursion | **Must** |
| [ ] | 90 | [Subsets II](https://leetcode.com/problems/subsets-ii/) | Medium | Sort + skip duplicates | Rec |
| [ ] | 46 | [Permutations](https://leetcode.com/problems/permutations/) | Medium | Used array backtracking | **Must** |
| [ ] | 39 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Medium | Reuse elements | **Must** |
| [ ] | 17 | [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Medium | Cartesian product backtracking | Rec |
| [ ] | 22 | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | Backtracking with counts | **Must** |
| [ ] | 79 | [Word Search](https://leetcode.com/problems/word-search/) | Medium | Grid DFS backtracking | **Must** |
| [ ] | 131 | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | Medium | Partition backtracking | Rec |

### 15. Graphs (DFS, BFS, Topological Sort, Shortest Path)

Grid and graph traversal, dependency ordering, and Dijkstra.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Grid DFS/BFS | **Must** |
| [ ] | 695 | [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | Medium | Grid DFS | Rec |
| [ ] | 133 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | Medium | DFS + hash map | **Must** |
| [ ] | 994 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | Multi-source BFS | **Must** |
| [ ] | 417 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Reverse DFS from borders | Rec |
| [ ] | 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Cycle detection / topo sort | **Must** |
| [ ] | 210 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Medium | Kahn's topological sort | Rec |
| [ ] | 743 | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Medium | Dijkstra | **Must** |
| [ ] | 787 | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Medium | Bellman-Ford / BFS levels | Adv |
| [ ] | 127 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | BFS on implicit graph | Adv |

### 16. Union-Find

Connected components and cycle detection. #721 is a good entity-resolution analogy for ML data cleaning.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 547 | [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Medium | Union-Find or DFS | **Must** |
| [ ] | 684 | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Medium | Union-Find cycle detection | Rec |
| [ ] | 721 | [Accounts Merge](https://leetcode.com/problems/accounts-merge/) | Medium | Union-Find on strings (entity resolution flavor) | **Must** |

### 17. Dynamic Programming: 1D

State definition, recurrence, and the 0/1 versus unbounded knapsack distinction.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | Fibonacci recurrence | **Must** |
| [ ] | 198 | [House Robber](https://leetcode.com/problems/house-robber/) | Medium | Take/skip DP | **Must** |
| [ ] | 213 | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | Medium | Circular DP | Rec |
| [ ] | 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Unbounded knapsack | **Must** |
| [ ] | 300 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | Medium | DP O(n^2) and binary search O(n log n) | **Must** |
| [ ] | 139 | [Word Break](https://leetcode.com/problems/word-break/) | Medium | String DP | **Must** |
| [ ] | 152 | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Medium | Track min and max | Rec |
| [ ] | 91 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | Medium | Counting DP | Rec |
| [ ] | 416 | [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Medium | 0/1 knapsack | **Must** |

### 18. Dynamic Programming: 2D & Strings

Grid DP and string-comparison DP (edit distance is the NLP-flavored classic).

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 62 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | Medium | Grid DP | **Must** |
| [ ] | 1143 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Medium | 2D string DP | **Must** |
| [ ] | 72 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Medium | 2D string DP (string similarity, NLP flavor) | **Must** |
| [ ] | 518 | [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Medium | Unbounded knapsack counting | Rec |

### 19. Design, Sampling & Math (ML-Flavored)

Caching, random sampling, and sorting fundamentals that map well to serving and data pipelines.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 384 | [Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) | Medium | Fisher-Yates shuffle | **Must** |
| [ ] | 398 | [Random Pick Index](https://leetcode.com/problems/random-pick-index/) | Medium | Reservoir sampling | Rec |
| [ ] | 528 | [Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) | Medium | Prefix sum + binary search (weighted sampling) | **Must** |
| [ ] | 380 | [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | Medium | Hash map + array swap-delete | **Must** |
| [ ] | 50 | [Pow(x, n)](https://leetcode.com/problems/powx-n/) | Medium | Fast exponentiation | Rec |
| [ ] | 912 | [Sort an Array](https://leetcode.com/problems/sort-an-array/) | Medium | Implement merge sort / quick sort | Rec |
| [ ] | 460 | [LFU Cache](https://leetcode.com/problems/lfu-cache/) | Hard | Frequency buckets + linked lists | Adv |

### 20. Bit Manipulation (Light Coverage)

Low priority for applied ML. A short pass is enough.

| Done | # | Problem | Difficulty | Key Pattern | Tier |
|---|---|---|---|---|---|
| [ ] | 136 | [Single Number](https://leetcode.com/problems/single-number/) | Easy | XOR | Rec |
| [ ] | 191 | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Easy | Bit counting | Rec |
| [ ] | 268 | [Missing Number](https://leetcode.com/problems/missing-number/) | Easy | XOR / sum formula | Rec |

---

## Beyond LeetCode: ML-flavored coding practice

Applied ML loops often mix standard algorithm questions with coding that is closer to the job. Confirm the format with your recruiter, and consider practicing a few of these from scratch in NumPy or PyTorch:

- k-nearest neighbors and k-means, including the distance computation and the update step
- Logistic regression with gradient descent, plus softmax and cross-entropy loss
- Evaluation metrics from scratch: precision, recall, F1, and ROC-AUC
- TF-IDF or a simple tokenizer and bag-of-words pipeline
- A basic attention layer or a small training loop, including debugging common shape and gradient mistakes
- Data wrangling in pandas and SQL: joins, group-by, and window functions

---

## How this list was built

<details>
<summary>Merge method, tier changes, and optional problems that were cut</summary>

### Sources

- **List A:** a 66-problem list organized by phase, with tiers Must, Recommended, and Advanced.
- **List B:** a 180-problem list (182 rows, 2 repeated) in 21 pattern-based sections.
- **Overlap:** all 66 problems in List A also appear in List B, so the merged list is List B refined, with no problems added from outside.

### What changed

- **Removed duplicates:** #981 (Time Based Key-Value Store) and #355 (Design Twitter) appeared twice in List B. Each now appears once, in its home section.
- **Cut 44 problems** that repeat a pattern already covered, are rarely asked for applied ML, or are premium-only (listed below). Of List A's 66 problems, 1 was cut (#312).
- **Moved to a better home:**
  - #53 Maximum Subarray moved from Greedy to section 2, since Kadane's algorithm is a fundamental.
  - #22 Generate Parentheses moved from Stack to Backtracking.
  - #394 Decode String moved from Strings to Stack.
  - #692 Top K Frequent Words moved from Arrays & Hashing to Heaps & Top-K.
  - #23 Merge k Sorted Lists moved from Linked List to Heaps & Top-K, since the heap solution is the point.
  - #146 LRU Cache moved from Design to Linked List, where its prerequisites live.
- **Merged the Design and Sampling sections** into one, and trimmed Bit Manipulation to three problems.
- **Re-sequenced** each section as a difficulty ramp rather than sorting by tier.

### Tier changes versus List B

- **Adv to Rec:** #2406
- **Must to Rec:** #76, #100, #210, #217, #226, #235, #242, #355, #684, #695
- **Rec to Adv:** #787
- **Rec to Must:** #721

Reasoning: Must is kept to the patterns most likely to be tested, so very easy warm-ups, near-repeats, and Hard problems with narrow payoff moved down. #721 moved up to Must because entity resolution maps closely to ML data cleaning. #2406 moved up to Rec because the minimum-groups sweep-line pattern is common in scheduling-style questions.

### Optional problems that were cut

Nothing here is wrong to solve. These are the first to add back if you have spare time.

| # | Problem | Why it was cut |
|---|---|---|
| 10 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard 2D DP, rarely asked |
| 16 | [3Sum Closest](https://leetcode.com/problems/3sum-closest/) | Variant of #15 |
| 25 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Pointer-manipulation Hard, low yield |
| 26 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Same read/write pointers as #283 |
| 36 | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | Hash-set pattern already covered; low ML relevance |
| 40 | [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | Variant of #90 |
| 41 | [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | Niche Hard (index-hashing trick) |
| 43 | [Multiply Strings](https://leetcode.com/problems/multiply-strings/) | Digit simulation, low yield |
| 51 | [N-Queens](https://leetcode.com/problems/n-queens/) | Rarely asked for applied ML |
| 64 | [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | Same grid DP as #62 |
| 66 | [Plus One](https://leetcode.com/problems/plus-one/) | Trivial carry handling |
| 97 | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | Hard 2D DP, rarely asked |
| 110 | [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | Same height-returning DFS as #543 |
| 115 | [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | Hard 2D DP, rarely asked |
| 130 | [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | Same border-DFS idea as #417 |
| 138 | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Hash-map cloning is covered by #133 |
| 312 | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Interval DP, rarely asked outside research-style loops |
| 332 | [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) | Niche Hard (Eulerian path) |
| 338 | [Counting Bits](https://leetcode.com/problems/counting-bits/) | Low-yield bit DP |
| 362 | [Design Hit Counter](https://leetcode.com/problems/design-hit-counter/) | Premium-only (cannot be opened on a free account) |
| 373 | [Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) | K-way heap pattern covered by #23 and #355 |
| 377 | [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) | Rarely asked |
| 438 | [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | Same fixed-window counting as #567 |
| 494 | [Target Sum](https://leetcode.com/problems/target-sum/) | Subset-sum variant covered by #416 |
| 496 | [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | Warm-up for #739, which already covers monotonic stack |
| 502 | [IPO](https://leetcode.com/problems/ipo/) | Niche Hard |
| 503 | [Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | Circular variant of #739, rarely asked |
| 525 | [Contiguous Array](https://leetcode.com/problems/contiguous-array/) | Same prefix-sum + hash map idea as #560 |
| 542 | [01 Matrix](https://leetcode.com/problems/01-matrix/) | Same multi-source BFS as #994 |
| 572 | [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | Composition of #100 |
| 647 | [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | Same expand-around-center idea as #5 |
| 724 | [Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) | Trivial prefix-sum variant of #303 |
| 746 | [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | Trivial variant of #70 |
| 785 | [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | Less common graph-coloring problem |
| 846 | [Hand of Straights](https://leetcode.com/problems/hand-of-straights/) | Niche greedy |
| 853 | [Car Fleet](https://leetcode.com/problems/car-fleet/) | Niche stack + sort problem |
| 876 | [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Trivial fast/slow pointer, covered by #141 |
| 1004 | [Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Variant of #424 |
| 1011 | [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Same binary-search-on-answer idea as #875 |
| 1046 | [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | Heap basics covered by #703 and #973 |
| 1202 | [Smallest String With Swaps](https://leetcode.com/problems/smallest-string-with-swaps/) | Niche Union-Find variant |
| 1448 | [Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | Same DFS-carrying-state idea as #98 |
| 1480 | [Running Sum of 1d Array](https://leetcode.com/problems/running-sum-of-1d-array/) | Trivial prefix-sum variant of #303 |
| 1631 | [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | Same Dijkstra pattern as #743 |

### Notes

- #362 (Design Hit Counter) is premium-only according to List B's own note, so it was cut. I have not verified the access status of every other problem, so check the padlock icon on LeetCode before starting one.
- I could not open LeetCode from my environment, so links were checked for consistency against the numbers and titles in List B but not tested live.

</details>
