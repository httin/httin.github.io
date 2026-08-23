---
layout: post
title: "Coordinate Compression"
description: "Large coordinates, few distinct values. Keep the order. Store the gaps."
date: 2026-08-20
thumbnail: /images/posts/coordinate-compression/coordinate-compression-poster.png
katex: 1
categories: ["Data Structures and Algorithms"]
tags: [algorithms, datastructures]
---

<!--more-->

## The problem

You get {% katex %}n{% endkatex %} updates and {% katex %}q{% endkatex %} queries on a number line.

- An update adds {% katex %}+1{% endkatex %} at coordinate {% katex %}x{% endkatex %}.
- A query asks how many updates are in the closed interval {% katex %}[L, R]{% endkatex %}.

**Constraints**

{% katex display %}
1 \le n, q \le 10^5
{% endkatex %}

{% katex display %}
1 \le x, L, R \le 10^9
{% endkatex %}

You need many updates and many range counts. A walk from {% katex %}L{% endkatex %} to {% katex %}R{% endkatex %} on each query is {% katex %}O(n){% endkatex %} per query. That is too slow at {% katex %}q = 10^5{% endkatex %}.

## A plain array, then prefix sums

Think of a row of boxes numbered {% katex %}1, \ldots, n{% endkatex %}. An update puts {% katex %}+1{% endkatex %} in one box. A query asks how many {% katex %}+1{% endkatex %} values are in the boxes {% katex %}[L, R]{% endkatex %}.

A plain array makes an update {% katex %}O(1){% endkatex %}: you write one slot. A query is {% katex %}O(n){% endkatex %}. You add every box from {% katex %}L{% endkatex %} to {% katex %}R{% endkatex %}.

Prefix sums make a query {% katex %}O(1){% endkatex %}: {% katex %}\mathrm{sum}[R] - \mathrm{sum}[L-1]{% endkatex %}. An update is {% katex %}O(n){% endkatex %}. You must rebuild many prefix sums.

You want both operations faster than {% katex %}O(n){% endkatex %}.

## Fenwick tree

A Fenwick tree (also called a Binary Indexed Tree) does both in {% katex %}O(\log n){% endkatex %} time. It is still an array. Slot {% katex %}i{% endkatex %} holds the sum of a short block of boxes that ends at {% katex %}i{% endkatex %}. To add at index {% katex %}i{% endkatex %}, you change a few slots. To get the sum of boxes {% katex %}[1, i]{% endkatex %}, you add a few other slots. The tree finds those slots from the binary form of {% katex %}i{% endkatex %}. The figure below uses {% katex %}n = 8{% endkatex %} so you can see every slot.

{% include image_full.html imageurl="/images/posts/coordinate-compression/fenwick-tree.png" title="Fenwick tree" caption="Top: the array a[1..8]. Middle: each coloured bar is one Fenwick slot and the block of a[] that it stores. Colour is the block length, equal to i & −i. Left: a prefix sum starts at i = 7 and repeats i = i − (i & −i). Right: an update at index 3 repeats i = i + (i & −i). Both walks touch O(log n) slots. A range sum is prefix(R) minus prefix(L−1)." %}

You do not need the bit rule for the rest of this post. Keep one fact: the slots are {% katex %}1, 2, \ldots, n{% endkatex %}. If {% katex %}n = 10^5{% endkatex %}, you allocate {% katex %}10^5{% endkatex %} slots. If you use a coordinate {% katex %}x = 10^9{% endkatex %} as the index, you allocate {% katex %}10^9{% endkatex %} slots. A segment tree has the same limit. A plain array has the same limit.

That is the gap that coordinate compression fills. It maps the large coordinates onto the small indices that these structures can use.

## BruteForce

Make an array {% katex %}\mathrm{freq}[10^9+1]{% endkatex %}. Add {% katex %}1{% endkatex %} at {% katex %}\mathrm{freq}[x]{% endkatex %}. After an {% katex %}O(10^9){% endkatex %} prefix-sum build, each query is {% katex %}O(1){% endkatex %}. That array holds four gigabytes of integers. You do not use most of them.

Most positions on the line are empty. If {% katex %}n = 10^5{% endkatex %}, then {% katex %}\le 10^5{% endkatex %} coordinates occur. The other positions stay empty.

The GIF below shows this with four updates, at {% katex %}x \in \{2, 7, 20, 23\}{% endkatex %}:

{% include image_full.html imageurl="/images/posts/coordinate-compression/rank-fold.gif" title="Rank compression" caption="Top axis: the original coordinates. Bottom axis: their ranks. The arrows keep a < b and remove b − a. After the map, an array of length 4 is sufficient." %}

## Rank compression

Collect each coordinate that you will use as an index. Sort the list. Remove duplicates. Replace each original value with its position in that list.

```cpp
vector<int> xs = {2, 7, 20, 23};          // every x, L, and R
sort(xs.begin(), xs.end());
xs.erase(unique(xs.begin(), xs.end()), xs.end());

auto rank = [&](int v) -> int {           // 1-based, for a Fenwick tree
    return int(lower_bound(xs.begin(), xs.end(), v) - xs.begin()) + 1;
};
```

Then {% katex %}\mathrm{rank}(2) = 1{% endkatex %}, {% katex %}\mathrm{rank}(7) = 2{% endkatex %}, {% katex %}\mathrm{rank}(20) = 3{% endkatex %}, {% katex %}\mathrm{rank}(23) = 4{% endkatex %}. The map keeps order: {% katex %}a < b \iff \mathrm{rank}(a) < \mathrm{rank}(b){% endkatex %}. The map does not keep distance. The gap {% katex %}20 - 7 = 13{% endkatex %} becomes {% katex %}3 - 2 = 1{% endkatex %}.

This is sufficient for a Fenwick tree that counts frequencies. Put each update and each query through `rank`. The tree then has size {% katex %}n{% endkatex %}, not {% katex %}10^9{% endkatex %}.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    vector<int> t;
    Fenwick(int n) : t(n + 1, 0) {}
    void add(int i, int v) { for (; i < (int)t.size(); i += i & -i) t[i] += v; }
    int sum(int i) { int s = 0; for (; i > 0; i -= i & -i) s += t[i]; return s; }
    int range(int l, int r) { return r < l ? 0 : sum(r) - sum(l - 1); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> upd(n);
    vector<pair<int, int>> qry(q);
    vector<int> xs;
    for (int i = 0; i < n; ++i) {
        cin >> upd[i];
        xs.push_back(upd[i]);
    }
    for (int i = 0; i < q; ++i) {
        cin >> qry[i].first >> qry[i].second;
        xs.push_back(qry[i].first);
        xs.push_back(qry[i].second);
    }
    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());
    auto rank = [&](int v) {
        return int(lower_bound(xs.begin(), xs.end(), v) - xs.begin()) + 1;
    };

    Fenwick bit((int)xs.size());
    for (int x : upd) bit.add(rank(x), 1);
    for (auto [L, R] : qry) {
        cout << bit.range(rank(L), rank(R)) << '\n';
    }
}
```

Errors that occur often:

**Compress the queries also.** `rank(L)` and `rank(R)` are correct only if {% katex %}L{% endkatex %} and {% katex %}R{% endkatex %} are in the sorted list. If you omit them, `lower_bound` still returns an index, but not the endpoint that you need. The code above puts each {% katex %}L{% endkatex %} and each {% katex %}R{% endkatex %} into `xs` before the sort.

**The interval is closed, so the two endpoints are values.** After you put each endpoint into `xs`, {% katex %}\mathrm{rank}(L){% endkatex %} is the first index with original coordinate {% katex %}\ge L{% endkatex %}. {% katex %}\mathrm{rank}(R){% endkatex %} is the last index with original coordinate {% katex %}\le R{% endkatex %}. That is why you add {% katex %}L{% endkatex %} and {% katex %}R{% endkatex %} as themselves. If you compress only the update coordinates, a query whose {% katex %}L{% endkatex %} is between two updates uses the wrong slot.

**Use 1-based ranks for a Fenwick tree.** `lower_bound` is 0-based. A Fenwick tree is not. You need the `+ 1`.

**You must know the values before you build the map.** This map is offline. If a query uses a coordinate that you did not store, you cannot find a rank. For true online input, use a dynamic segment tree, a treap, or an ordered set. Do not use this map.

## What the map removes

The GIF fold removes each gap. For a frequency query, that is correct. You count points. Points have no width.

Use the same four coordinates with two intervals, {% katex %}[2, 7){% endkatex %} and {% katex %}[20, 23){% endkatex %}. Now find the covered length.

{% include image_full.html imageurl="/images/posts/coordinate-compression/coverage-weights.gif" title="Coverage after compression" caption="The intervals use the same fold. After ranking, each interval looks one unit long. That count is wrong. The green weights xs[i+1] − xs[i] put the gaps back as edge costs. Covered length is 5 + 3 = 8 again." %}

The true covered length is {% katex %}5 + 3 = 8{% endkatex %}. After ranking, the intervals become {% katex %}[1, 2){% endkatex %} and {% katex %}[3, 4){% endkatex %}. If you set each compressed cell to length {% katex %}1{% endkatex %}, you get {% katex %}2{% endkatex %}.

Keep the original coordinates with the ranks. Treat the compressed line as a path with weights:

{% katex display %}
w(i \rightarrow i+1) = x_s[i+1] - x_s[i]
{% endkatex %}

A move from rank {% katex %}1{% endkatex %} to rank {% katex %}2{% endkatex %} still covers {% katex %}5{% endkatex %} units. A move from rank {% katex %}3{% endkatex %} to rank {% katex %}4{% endkatex %} still covers {% katex %}3{% endkatex %}. The gap {% katex %}13{% endkatex %} stays on the edge between ranks {% katex %}2{% endkatex %} and {% katex %}3{% endkatex %}. You do not walk that edge if you only cover the two intervals.

The [line sweep](/Line-Sweep-Algorithm) post ends with the same pattern: union of rectangle areas. The sweep still reads events in {% katex %}x{% endkatex %} order. The active set still needs a segment tree on {% katex %}y{% endkatex %}. You cannot index that tree with raw {% katex %}y{% endkatex %} when {% katex %}|y| \le 10^9{% endkatex %}. Rank the {% katex %}y{% endkatex %} coordinates. Give each compressed segment the original gap as its weight. Then the covered area is in real units, not in ranks.

## A maze that is mostly empty

The same fold works in two dimensions. I first saw this on a grid that was too large for BFS. The rooms were large. The walls were few. The shortest path turns only at a boundary.

{% include image_full.html imageurl="/images/posts/coordinate-compression/coordinate-compression-poster.png" title="Coordinate compression poster" caption="Empty space is removed. The walls, the start, and the end keep their relative order." %}

{% include image_full.html imageurl="/images/posts/coordinate-compression/maze-compress.gif" title="Maze coordinate compression" caption="Identical consecutive rows become one compressed row. Then the same occurs for columns. One colour on the left is one cell of that colour on the right. Orange is the shortest path. One step on the compressed maze can cover many original cells, so the edges have weights. Use Dijkstra, not BFS." %}

Scan the rows from top to bottom. Keep a row when it is different from the row above it. A sequence of identical empty rows becomes one compressed row. Do the same for columns. The compressed grid is small enough to search. The shape does not change. Each coloured region on the left is one cell of that colour on the right.

A compressed step can cover many original cells, so the edges do not all have cost {% katex %}1{% endkatex %}. BFS on the compressed maze counts cells. That is the same error as the covered-length example. Dijkstra counts distance if the edge weight is the original width or height of that step.

## Why extra splits

If you rank only the wall coordinates, a shortest path that turns can fail. Two cells can share a compressed column and have different neighbours.

{% include image_full.html imageurl="/images/posts/coordinate-compression/split-neighbors.png" title="Keep c-1, c, and c+1" caption="The two red cells are in the same column. The left cell cannot go through the wall. The right cell can, because it is in the opening. If those two rows become one compressed row, the cell has two neighbourhoods. Dijkstra cannot tell them apart. Keep the row above the change, the change, and the row below the change: c−1, c, and c+1." %}

The cell next to the wall can move only along the wall. The cell next to the opening can go through the opening. If you merge those rows, the compressed cell is not correct. Some original positions in it can leave. Some cannot.

Do this: take each coordinate {% katex %}c{% endkatex %} where the maze changes. Also keep {% katex %}c-1{% endkatex %} and {% katex %}c+1{% endkatex %}. Duplicate splits become one split. Then each compressed cell contains only original positions that have the same neighbourhood. A path that must turn still has a vertex for that turn.

The compression does not remove routes. It groups positions that behave the same, and it writes the real travel cost on the edges between groups. Use Dijkstra on the compressed graph. Use BFS on the original graph.

## When compression does not help

Use compression when the value range is large and the set of values that occur is small.

Do not use compression when the **range is already dense**. If each {% katex %}x{% endkatex %} is already in {% katex %}1..n{% endkatex %}, ranking does no work and adds code.

Do not use compression when you **need the numbers**. Hashing, XOR of values, and "sum of the original coordinates in this range" use {% katex %}x{% endkatex %}, not {% katex %}\mathrm{rank}(x){% endkatex %}. You can still rank for the index and store {% katex %}x{% endkatex %} in an array. Do not replace {% katex %}x{% endkatex %} with the rank.

Do not use compression on a **dense maze**. If almost each row is different from the next row, the compressed grid is the original grid plus a sort. Use compression on a graph that has large empty space.

Before you write the map, answer two questions. Do you need only order, or do you also need distance? Did you collect each coordinate that you will use as an index? For a frequency Fenwick tree you need only order, and the query endpoints go in the list. For covered length and maze shortest path you need order and distance, so the original coordinates stay as weights. For online queries of new coordinates, this map is the wrong tool.

## Practice

- [Advent of Code 2025, Day 9](https://adventofcode.com/2025/day/9): the movie-theater floor. I personally like this problem. There are few red tiles, but the grid is large. Part 1: use each pair of red tiles as opposite corners of a rectangle. The area uses the original gaps, so keep {% katex %}x{% endkatex %} and {% katex %}y{% endkatex %}. Part 2: the rectangle must stay in the boundary that the red tiles make. You cannot fill a {% katex %}10^6 \times 10^6{% endkatex %} floor. Rank the two axes. Fill the compressed grid. Give each cell a weight equal to the number of real tiles that it contains.
- [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/): Fenwick tree on ranks, from right to left. The [ordered set](/Ordered-Set-data-structure-in-C++) post solves the same problem with a different tree.
- [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/): the sweep from the line-sweep post, with heights as the compressed coordinate.
- [Rectangle Area II](https://leetcode.com/problems/rectangle-area-ii/): union of rectangle areas. Sweep on {% katex %}x{% endkatex %}. Use a segment tree on compressed {% katex %}y{% endkatex %}. Set edge weights to {% katex %}y_{i+1} - y_i{% endkatex %}.
- A sparse maze whose BFS does not fit in memory: compress rows and columns, keep {% katex %}c-1, c, c+1{% endkatex %} around every wall, Dijkstra with the original widths as edge weights. [Magnus's write-up](https://mhh.dev/code-challenge/2026/06/24/coordinate-compression.html) is the one that made the extra splits click for me.
