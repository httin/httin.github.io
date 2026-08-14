---
layout: post
title: "Line Sweep Algorithm"
description: "A moving vertical line turns a quadratic geometry problem into an ordered pair."
date: 2026-08-11
thumbnail: /images/posts/line-sweep/closest-pair-sweep-poster.png
katex: 1
categories: ["Data Structures and Algorithms"]
tags: [algorithms, geometry]
---

The line sweep is a standard way to turn a 2D geometry problem into a sorted sequence of events. You pick an axis, sort by it, and walk through the input once while maintaining a set of objects that are still relevant. For closest pair, that set stays small enough that each step is cheap.

<!--more-->

## The problem

Given {% katex %}n{% endkatex %} points on the {% katex %}Oxy{% endkatex %} plane, with distance defined as Euclidean distance, find the pair of points closest together.

**Input**

- The first line contains a positive integer {% katex %}n{% endkatex %}, the number of points.
- Each of the next {% katex %}n{% endkatex %} lines contains two integers {% katex %}x_i, y_i{% endkatex %}, the coordinates of point {% katex %}i{% endkatex %}.

**Constraints**

{% katex display %}
1 \le n \le 50000
{% endkatex %}

{% katex display %}
|x_i|, |y_i| \le 10^6 \quad \forall i: 1 \le i \le n
{% endkatex %}

**Output**

Print the indices {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %} of the closest pair, and the distance between them, rounded to 6 decimal places.

## BruteForce

Two loops. Check every pair, keep the smallest.

At {% katex %}n = 50000{% endkatex %} that is {% katex %}\frac{n(n-1)}{2} = 1{,}249{,}975{,}000{% endkatex %} pairs.

On my laptop, the brute force finishes in 0.57 seconds, because the inner loop is simple integer arithmetic and the compiler vectorises it well.

Here is the brute force against the sweep

| {% katex %}n{% endkatex %} | brute force | line sweep |
|---|---|---|
| 12500 | 0.06s | 0.02s |
| 25000 | 0.16s | 0.04s |
| 50000 | 0.57s | 0.09s |
| 100000 | 2.13s | 0.18s |
| 200000 | 8.55s | 0.36s |

When {% katex %}n{% endkatex %} doubles, the brute force time roughly quadruples. The sweep time roughly doubles.

Most of that work is wasted. Once you have found a pair at distance 40, there is no point checking two points a million units apart.

## Sweep Line

Sort the points by {% katex %}x{% endkatex %}, then walk a vertical line left to right. At each stop, keep a running best distance {% katex %}d{% endkatex %} and only compare against points that can still beat it.

{% include image_full.html imageurl="/images/posts/line-sweep/closest-pair-sweep-poster.png" title="Closest pair line sweep, final step" caption="Step 10/10 at point H. Red: sweep line and current point. Blue: active set. Green box: candidate band (width d, height 2d). Orange: best pair so far." %}

{% include image_full.html imageurl="/images/posts/line-sweep/closest-pair-sweep.gif" title="Closest pair line sweep animation" caption="All ten steps. Gray points were evicted because they are farther than d behind the line." %}

The animation uses this input (already sorted by {% katex %}x{% endkatex %}): A(1,1), B(2,5), C(3,2), E(5,2), I(6,3), D(6,6), J(7,1), F(9,1), G(11,7), H(13,2).

We observe the following. At step {% katex %}i{% endkatex %}, we have already examined {% katex %}i - 1{% endkatex %} points. Let {% katex %}d{% endkatex %} be the smallest distance among all pairs formed from those points. For point {% katex %}P(x_i, y_i){% endkatex %}, the task is to find whether there exists a point {% katex %}X{% endkatex %} among those {% katex %}i - 1{% endkatex %} points such that {% katex %}XP < d{% endkatex %}.

Any point {% katex %}(x_j, y_j){% endkatex %} with {% katex %}j < i{% endkatex %} where {% katex %}x_j < x_i - d{% endkatex %} (too far to the left) or {% katex %}y_j < y_i - d\:||\:y_j > y_i + d{% endkatex %} (too far below or above) cannot qualify. We only need to check points inside the rectangle with corners {% katex %}(x_i - d, y_i - d){% endkatex %}, {% katex %}(x_i - d, y_i + d){% endkatex %}, {% katex %}(x_i, y_i - d){% endkatex %}, and {% katex %}(x_i, y_i + d){% endkatex %}, the green box in the figure. How many points can lie in this rectangle? If the region holds thousands of points, the algorithm will be slow.

## How many candidates

The complexity argument depends on the candidate box staying small. Fortunately, there is an upper bound, a constant that doesn't grow with {% katex %}n{% endkatex %}.

**Claim.** At each point {% katex %}p{% endkatex %} being processed, to find a pair closer than {% katex %}d{% endkatex %}, we only need to check at most 6 other points.

**Proof.** Every point in the active set has already been processed, and {% katex %}d{% endkatex %} is the minimum distance over all processed pairs. So every two points in the active set are at least {% katex %}d{% endkatex %} apart.

The box is {% katex %}d{% endkatex %} wide and {% katex %}2d{% endkatex %} tall. Cut it into a 2x3 grid, giving 6 cells, each {% katex %}\frac{d}{2}{% endkatex %} wide and {% katex %}\frac{2d}{3}{% endkatex %} tall. The longest distance inside one cell is its diagonal:

{% katex display %}
\sqrt{\left(\frac{d}{2}\right)^2 + \left(\frac{2d}{3}\right)^2} = \sqrt{\frac{d^2}{4} + \frac{4d^2}{9}} = \sqrt{\frac{9d^2 + 16d^2}{36}} = \sqrt{\frac{25d^2}{36}} = \frac{5d}{6}
{% endkatex %}

And {% katex %}\frac{5d}{6} < d{% endkatex %}. Two points in the same cell would be closer than {% katex %}d{% endkatex %}, a contradiction since {% katex %}d{% endkatex %} is the minimum distance found so far. So each cell holds at most one point, and the box holds at most 6. {% katex %}\blacksquare{% endkatex %}

The constant 6 is a chosen number with mathematic proof, it's not always fixed for this algorithm. In practice the box is usually much smaller. Over random inputs the maximum observed was 3. On a triangular lattice, which is the densest possible packing at minimum distance {% katex %}d{% endkatex %}, the maximum was 2.

Overall: {% katex %}n{% endkatex %} insertions, {% katex %}n{% endkatex %} deletions, and {% katex %}n{% endkatex %} range queries, each {% katex %}O(\log n){% endkatex %}, with a constant amount of distance arithmetic per point. Plus the sort. That is {% katex %}O(n \log n){% endkatex %}.

## The algorithm

1. Sort the points by increasing {% katex %}x{% endkatex %}.
2. Walk through the sorted list, maintaining a `std::set` {% katex %}s{% endkatex %} of active points (ordered by {% katex %}y{% endkatex %}, so each band lookup is a range query rather than a full scan).
3. Let {% katex %}d{% endkatex %} be the best distance found so far. At each step, for point {% katex %}p_i{% endkatex %}:
   - Remove from {% katex %}s{% endkatex %} any point whose {% katex %}x{% endkatex %} is more than {% katex %}d{% endkatex %} behind {% katex %}p_i{% endkatex %}.
   - Among the points left in {% katex %}s{% endkatex %} with {% katex %}|q.y - p_i.y| \le d{% endkatex %}, compute the distance to {% katex %}p_i{% endkatex %} and update {% katex %}d{% endkatex %} if any pair is closer.
   - Insert {% katex %}p_i{% endkatex %} into {% katex %}s{% endkatex %}.

## The code (C++)

`std::set` gives {% katex %}O(\log n){% endkatex %} insert, erase, and `lower_bound` for the band lookup.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Point {
    int x, y, id;

    bool operator<(const Point& other) const {
        return x != other.x ? x < other.x : y < other.y;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Point> p(n);
    for (int i = 0; i < n; ++i) {
        cin >> p[i].x >> p[i].y;
        p[i].id = i + 1;               // the statement wants 1-based indices
    }
    if (n < 2) return 0;               // n = 1 is legal, and has no pair

    sort(p.begin(), p.end());

    auto sq = [](long long v) { return v * v; };
    auto dist2 = [&](int a, int b) {   // dist2 means squared distance, returning dx² + dy²
        return sq(p[a].x - p[b].x) + sq(p[a].y - p[b].y);
    };

    long long d2 = dist2(0, 1);        // seed with the first pair; n >= 2 here
    int ansA = p[0].id, ansB = p[1].id;

    set<pair<int, int>> active;        // (y, position); when points in the set have the same y, they sit in index order: (y, 0), (y, 2), (y, 5), ...
    active.insert({p[0].y, 0});
    active.insert({p[1].y, 1});

    int left = 0;
    for (int i = 2; i < n; ++i) {
        // 1. Retire points too far left.
        while (left < i && sq(p[i].x - p[left].x) >= d2) {
            active.erase({p[left].y, left});
            ++left;
        }

        // 2. Half-height of the band: ceil(sqrt(d2)).
        long long d = (long long)sqrt((double)d2);
        while (d * d < d2) ++d;

        // 3. Walk the band. At most six points live here.
        auto it = active.lower_bound({(int)(p[i].y - d), INT_MIN});
        for (; it != active.end() && it->first <= p[i].y + d; ++it) {
            const Point& q = p[it->second];
            long long dist = sq(p[i].x - q.x) + sq(p[i].y - q.y);
            if (dist < d2) {
                d2 = dist;
                ansA = q.id;
                ansB = p[i].id;
            }
        }

        active.insert({p[i].y, i});
    }

    if (ansA > ansB) swap(ansA, ansB);
    cout << ansA << ' ' << ansB << '\n'
         << fixed << setprecision(6) << sqrt((double)d2) << '\n';
    return 0;
}
```

A few implementation details that are easy to get wrong:

**Seed `d2` from the first two points.** After sorting, `p[0]` and `p[1]` are the leftmost pair, so their squared distance is a valid starting value for {% katex %}d^2{% endkatex %}. The main loop then starts at {% katex %}i = 2{% endkatex %} with both points already in the active set.

**Compare squared distances, not lengths.** With {% katex %}|x|, |y| \le 10^6{% endkatex %}, every squared distance fits in a `long long`. Store it as `d2`; the inner loop stays exact integer arithmetic, and `sqrt` is only for the band width and the final output.

**The window is a two-pointer.** `left` only ever moves forward, so each point is erased exactly once across the entire run. If you rebuild the window per point instead, you have written the quadratic loop again with a `std::set` bolted on.

**Key the set on `(y, position)`.** Points share {% katex %}y{% endkatex %} values constantly. With a bare {% katex %}y{% endkatex %} key, a `set` silently drops the duplicates and an erase removes the wrong point. The position makes every key unique and gives you a way back to the coordinates.

**Round the band up, not down.** Building the `lower_bound` key needs a real length, so `d` has to be {% katex %}\lceil\sqrt{d^2}\rceil{% endkatex %}. Rounding up is safe: it can only widen the band, and every candidate is re-checked with exact integer arithmetic anyway. Rounding down can push the true closest pair outside the band and lose the answer.

An edge case in the constraints: duplicate points drive `d2` to 0, and then the eviction test `dx*dx >= 0` is always true, so the active set empties on every step. That stays correct and stays linear, since each point is still erased only once.

## The same pattern elsewhere

The pattern is:

1. Turn the input into events along one axis.
2. Sort them.
3. Sweep, holding an active set of everything still relevant.
4. Define what enters the set and what leaves it.
5. Answer a cheap query against the set at each event.

Step 3 is where the problems differ. Here are two common cases.

### The active set is just a counter

Given {% katex %}n{% endkatex %} intervals {% katex %}[s_i, e_i]{% endkatex %}, what is the largest number of them that overlap at one point?

You do not need the intervals themselves. You need the moments the count changes. Each interval contributes `+1` when it opens and `-1` when it closes. Sort the {% katex %}2n{% endkatex %} events, run a counter, take the maximum.

```cpp
vector<pair<int, int>> ev;                 // (coordinate, delta)
for (auto& [s, e] : intervals) {
    ev.push_back({s, +1});
    ev.push_back({e, -1});
}

// Closed intervals [s,e]: an interval starting where another ends DOES
// overlap, so +1 must land before -1 at equal coordinates.
// For half-open [s,e), flip this comparison.
sort(ev.begin(), ev.end(), [](const pair<int,int>& a, const pair<int,int>& b) {
    return a.first != b.first ? a.first < b.first : a.second > b.second;
});

int cur = 0, best = 0;
for (auto& [pos, delta] : ev) {
    cur += delta;
    best = max(best, cur);
}
```

The comparator's second branch is the whole problem. When one interval ends exactly where the next begins, do they overlap? For closed intervals, yes, and opens must be processed first. For half-open intervals, a meeting room freed at 10:00 and booked at 10:00 does not conflict, so closes go first. Sort on coordinate alone and tied events land in arbitrary order is wrong in general.

No extra data structure is needed here. Sorting and a counter are enough.

### The active set is ordered, and the order changes

Given {% katex %}n{% endkatex %} line segments, does any pair of them cross? The obvious approach tests {% katex %}O(n^2){% endkatex %} pairs.

Events: the {% katex %}2n{% endkatex %} endpoints, sorted by {% katex %}x{% endkatex %}. Active set: the segments the sweep line currently crosses, ordered by the {% katex %}y{% endkatex %} at which each one crosses that line.

Two segments can only cross if they become vertical neighbours in that ordering at some moment before they cross. So you never compare all pairs. On a left endpoint, insert the segment and test it only against the segment directly above and the one directly below. On a right endpoint, remove it and test the two segments that just became neighbours. Stop at the first hit. That is Shamos and Hoey, {% katex %}O(n \log n){% endkatex %}.

The comparator is tricky here too. The sort key is "y at the current sweep position", so the key changes as the line moves, and two segments genuinely swap places when they cross. For detection you can stop at the first crossing, so no swap ever has to be handled. If you want to *enumerate* every intersection you need Bentley-Ottmann, which feeds intersection points back in as new events and swaps the pair inside the active set. Decide which of the two problems you have before you start, because the data structure requirements are different.

## When the sweep does not help

The sweep works when relevance is local along some axis and objects leave the active set at a predictable time. Closest pair works because a better answer has to be nearby, and "nearby" keeps shrinking. Interval overlap works because an interval stops mattering the instant it closes.

It does not help when the **active set cannot be bounded**, or when the **per-event query is not cheap**. If every event has to look at everything still active, you have rewritten the {% katex %}O(n^2){% endkatex %} loop with a {% katex %}\log n{% endkatex %} factor stapled on top and a lot more code to get wrong.

Before writing a sweep, answer two questions: **what leaves the active set, and what makes the query cheap?** For closest pair the answers are "points further than {% katex %}d{% endkatex %} behind the line" and "the band holds at most 6 points". If you cannot answer both for your problem, look for a different invariant first.

## Practice

- [My Calendar II](https://leetcode.com/problems/my-calendar-ii/description/)
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)
- [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/): the active set becomes a multiset of heights.
- Union of rectangle areas: the natural next step, where the active set needs a segment tree over compressed coordinates.
