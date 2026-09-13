---
layout: post
title: "Stack, Queue, and Deque"
description: "LIFO, FIFO and double-ended queues; DFS, BFS, and sliding window."
date: 2023-12-30
thumbnail: /images/posts/stack-queue-deque/stack-queue-deque-poster.png
katex: 1
categories: ["Data Structures and Algorithms"]
tags: [algorithms, datastructures, graph]
---

This post covers `std::stack`, `std::queue`, and `std::deque`. I will walk you through each data structure, how it applies, and its methods with Big-O complexity. In summary, a stack only uses one end, a queue pushes on the back and pops from the front, and a deque can do either.

<!--more-->

{% include image_full.html imageurl="/images/posts/stack-queue-deque/stack-queue-deque-poster.png" title="Stack, queue, deque" caption="A stack pops the newest item. A queue pops the oldest. A deque can do either." %}

## The problem

You are walking a graph. From a node you can leave on several edges, so you have to choose an order.

Two orders show up all the time. Depth-first search finishes the current branch before it tries the next one. Breadth-first search finishes every node at distance {% katex %}k{% endkatex %} before it looks at distance {% katex %}k+1{% endkatex %}.

I will use this undirected graph for both:

{% katex display %}
\begin{aligned}
A &\colon \{B, C\} \\
B &\colon \{A, D, E\} \\
C &\colon \{A, F\} \\
D &\colon \{B\} \\
E &\colon \{B\} \\
F &\colon \{C\}
\end{aligned}
{% endkatex %}

Start at {% katex %}A{% endkatex %}.

If you recurse from {% katex %}A{% endkatex %}, you visit {% katex %}A, B, D, E, C, F{% endkatex %}. The runtime keeps unfinished calls on the call stack. The next section does the same walk with `std::stack`.

## Stack

`std::stack` is last-in, first-out. Insert and remove at one end, called the top.

### DFS

Put {% katex %}A{% endkatex %} on the stack. While the stack is not empty, pop a node, mark it visited, and push the neighbours that are not seen. Push them in reverse adjacency order so the first neighbour lands on top. Then the walk matches the recursive one.

{% include image_full.html imageurl="/images/posts/stack-queue-deque/dfs-stack.gif" title="DFS with a stack" caption="Blue nodes are still on the stack. Green nodes were just pushed. Orange is the path from A to the current node. Visit order: A, B, D, E, C, F." %}

```cpp
vector<int> dfs(int start, const vector<vector<int>>& g) {
    vector<char> seen(g.size(), 0);
    vector<int> order;
    stack<int> st;
    st.push(start);
    while (!st.empty()) {
        int u = st.top();
        st.pop();
        if (seen[u]) continue;
        seen[u] = 1;
        order.push_back(u);
        for (int i = (int)g[u].size() - 1; i >= 0; --i) {
            int v = g[u][i];
            if (!seen[v]) st.push(v);
        }
    }
    return order;
}
```

Easy mistakes:

**No iterators.** You cannot browse a `std::stack`. If you need the values later, store them yourself. Or init the stack with a `vector` container, then read `back()`.

**In a contest, a `vector` is usually the better stack.** `std::stack` is an adapter where the default inner container is `deque`. What you want most of the time is `vector` plus `push_back` / `pop_back`: one contiguous buffer, nicer cache behaviour, and you can print the contents when something looks off.

**A long recursion can overflow.** Each recursive call adds a frame to the call stack (return address, arguments, locals). Stack memory is small and fixed so {% katex %}10^5{% endkatex %} nested calls usually do not fit. `std::stack` grows on the heap memory, so it's fine.

### Methods and complexity

`std::stack<T, Container>` forwards every call to `Container`. With the default `deque`, or with `vector`:

| Method | What it does | Time |
|---|---|---|
| `empty()` | true when there are no elements | {% katex %}O(1){% endkatex %} |
| `size()` | number of elements | {% katex %}O(1){% endkatex %} |
| `top()` | reference to the newest element | {% katex %}O(1){% endkatex %} |
| `push(x)` / `emplace(...)` | insert at the top | amortised {% katex %}O(1){% endkatex %} |
| `pop()` | remove the newest element | {% katex %}O(1){% endkatex %} |
| `swap(other)` | swap with another stack | {% katex %}O(1){% endkatex %} |

There is no `operator[]`, and no insert in the middle. If you need those, pick a different container.

`emplace` builds the element in place. `push` copies or moves an object you already have. For an `int` they cost the same. For a fat `pair` or a string, `emplace` skips a temporary.

### Underlying structure

`std::stack` does not store the elements itself. It is a thin wrapper around another container and only calls `back`, `push_back`, and `pop_back` on it. The default inner container is `deque`. You can pass `vector` instead: `stack<int, vector<int>>`. A stack never needs the front, so `vector` is the usual choice.

## Queue

`std::queue` is first-in, first-out. Insert at the back, remove at the front.

### BFS

Use the graph above and start at {% katex %}A{% endkatex %} again. Swap the stack for a queue and do not reverse the neighbour list. Mark a node the first time you enqueue it, so it never goes in twice.

{% include image_full.html imageurl="/images/posts/stack-queue-deque/bfs-queue.gif" title="BFS with a queue" caption="The frontier is now a queue: the oldest node leaves first. Start with A, then its children, then theirs. Visit order: A, B, C, D, E, F." %}

```cpp
vector<int> bfs(int start, const vector<vector<int>>& g) {
    vector<char> seen(g.size(), 0);
    vector<int> order;
    queue<int> q;
    q.push(start);
    seen[start] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : g[u]) {
            if (!seen[v]) {
                seen[v] = 1;
                q.push(v);
            }
        }
    }
    return order;
}
```

In the DFS GIF, {% katex %}C{% endkatex %} waits until {% katex %}B{% endkatex %}'s subtree is done. In the BFS GIF, {% katex %}C{% endkatex %} comes right after {% katex %}B{% endkatex %}, because both are one hop from {% katex %}A{% endkatex %}.

On an unweighted graph that is also a shortest path. The first time you dequeue a node, every closer node has already come out. Store the hop count when you enqueue.

Easy mistakes:

**Mark seen on enqueue, not on dequeue.** If you wait until `pop`, the same node can sit in the queue once per incoming edge. This may cost {% katex %}O(n^2){% endkatex %} you on a dense graph.

### Methods and complexity

The adapter forwards to `Container` again. With `deque`:

| Method | What it does | Time |
|---|---|---|
| `empty()` | true when there are no elements | {% katex %}O(1){% endkatex %} |
| `size()` | number of elements | {% katex %}O(1){% endkatex %} |
| `front()` | reference to the oldest element | {% katex %}O(1){% endkatex %} |
| `back()` | reference to the newest element | {% katex %}O(1){% endkatex %} |
| `push(x)` / `emplace(...)` | insert at the back | amortised {% katex %}O(1){% endkatex %} |
| `pop()` | remove the oldest element | {% katex %}O(1){% endkatex %} |
| `swap(other)` | swap with another queue | {% katex %}O(1){% endkatex %} |

`pop` does not return a value. Read `front`, then `pop`.

### Underlying structure

Default inner container: `deque`. Same chunks as in the next section. The queue only lets you insert at one end and remove at the other, so you cannot use `operator[]` even though the `deque` underneath has it.

If you need the smallest remaining key instead of the oldest, use `priority_queue`, also known as a heap. [Dijkstra](https://cp-algorithms.com/graph/dijkstra.html) is BFS with that heap in place of the queue.

## Deque

`std::deque` is a double-ended queue. You can insert, remove, and read at both ends, and you can index.

DFS only needed `push` and `pop` on one end. BFS needed `pop_front` and `push_back`. But a sliding window also pops from the back, so you want a deque.

### A window that slides one way

You have an array {% katex %}a[0..n){% endkatex %} and a width {% katex %}k{% endkatex %}. For every {% katex %}i{% endkatex %} with {% katex %}i \ge k-1{% endkatex %}, report {% katex %}\max(a[i-k+1], \ldots, a[i]){% endkatex %}.

{% katex display %}
n \le 10^5
{% endkatex %}

First approach, a loop over the window at each {% katex %}i{% endkatex %} is {% katex %}O(nk){% endkatex %}. Too slow.

Second approach, push each {% katex %}(a[i], i){% endkatex %} into a max heap. After the push, if the largest (i.e. top) element's index is less than {% katex %}i-k+1{% endkatex %}, it has left the window, so pop it; we keep this process until the top is inside and this value is the answer. Smaller items that already slid out can sit in the heap as they are not on top, so they never get reported. Each step is a heap push plus a few pops, so the pass is {% katex %}O(n \log n){% endkatex %}.

Third approach, keep a deque of indices whose values go downhill: {% katex %}a[\mathrm{front}] \ge a[\mathrm{next}] \ge \cdots{% endkatex %}. The front is the current maximum.

- When the front index falls out of {% katex %}[i-k+1, i]{% endkatex %}, `pop_front`.
- From the back, `pop_back` while {% katex %}a[\mathrm{back}] \le a[i]{% endkatex %}. Those values cannot be the max any more.
- `push_back(i)`.
- If the window is full, the answer is {% katex %}a[\mathrm{front}]{% endkatex %}.

Each index is pushed once and popped once. The whole pass is {% katex %}O(n){% endkatex %}.

{% include image_full.html imageurl="/images/posts/stack-queue-deque/sliding-window-deque.gif" title="Monotonic deque, sliding window maximum" caption="Array [1, 3, −1, −3, 5, 3, 6, 7] and k = 3. The blue box is the window. The deque stores indices; the orange cell at the front is the maximum." %}

```cpp
vector<int> window_max(const vector<int>& a, int k) {
    deque<int> dq;                       // indices, a[dq] is decreasing
    vector<int> ans;
    for (int i = 0; i < (int)a.size(); ++i) {
        if (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) ans.push_back(a[dq.front()]);
    }
    return ans;
}
```

Easy mistakes:

**Decreasing for a maximum, increasing for a minimum.** Flip the comparison and you get the other one. Do not store raw values if two equal values can sit in the window. You would not know which index to expire.

**`<=` versus `<`.** With `<=` you drop an older equal value and keep the newer index. The older one leaves the window first anyway.

**Do not keep pointers or iterators into a `deque` across an insert.** `push_front` or `push_back` may allocate a new block and invalidate iterators. References to existing elements stay valid on an end insert. Insert or erase in the middle invalidates everything. If you need a stable address, use a `list`, or a `vector` of values you never move.

### Methods and complexity

`deque` is a real container, not an adapter, so there are more methods.

**Element access**, all {% katex %}O(1){% endkatex %}:

| Method | What it does |
|---|---|
| `operator[](i)` | unchecked access |
| `at(i)` | checked access; throws `out_of_range` |
| `front()` / `back()` | first and last element |

**Iterators.** `begin`, `end`, `rbegin`, `rend`, and the `c` / `cr` variants are {% katex %}O(1){% endkatex %} to obtain. Walking {% katex %}k{% endkatex %} steps is {% katex %}O(k){% endkatex %}. The iterators are random access, so `it + k` is {% katex %}O(1){% endkatex %}.

**Capacity**

| Method | Time |
|---|---|
| `empty()`, `size()`, `max_size()` | {% katex %}O(1){% endkatex %} |
| `shrink_to_fit()` | up to {% katex %}O(n){% endkatex %}, may reallocate |
| `resize(n)` | linear in the number of inserted or erased elements |

**Modifiers**

| Method | Time |
|---|---|
| `push_front` / `push_back` / `emplace_front` / `emplace_back` | amortised {% katex %}O(1){% endkatex %} |
| `pop_front` / `pop_back` | {% katex %}O(1){% endkatex %} |
| `insert` / `emplace` / `erase` in the middle | {% katex %}O(n){% endkatex %}: linear in the distance to the nearer end |
| `clear` | {% katex %}O(n){% endkatex %} |
| `assign` | {% katex %}O(n){% endkatex %} |
| `swap` | {% katex %}O(1){% endkatex %} |

`insert` in the middle is slow on both `deque` and `vector`. Use a `deque` when you need `push_front`.

### Underlying structure

I am looking at GNU libstdc++ here ([`<bits/stl_deque.h>`](https://github.com/gcc-mirror/gcc/blob/releases/gcc-14.2.0/libstdc++-v3/include/bits/stl_deque.h#L507)).

A `deque<T>` is an array of pointers, `_M_map`, and each pointer owns a fixed block of `T`. The file even warns that "map" has nothing to do with `std::map`. Think of a table of contents: the map says which blocks exist, the blocks hold the values.

```cpp
struct _Deque_impl_data {
    T**    _M_map;       // array of pointers to blocks
    size_t _M_map_size;  // how many pointer slots, at least 8
    iterator _M_start;   // first live element
    iterator _M_finish;  // one past the last live element
};
```

Block length is a compile-time rule, about 512 bytes of `T`:

```cpp
#ifndef _GLIBCXX_DEQUE_BUF_SIZE
#define _GLIBCXX_DEQUE_BUF_SIZE 512
#endif

inline size_t __deque_buf_size(size_t __size) {
    return __size < 512 ? size_t(512 / __size) : size_t(1);
}
```

So `deque<int>` (4 bytes) packs 128 ints in a block. A type larger than 512 bytes gets one element per block. The first and last blocks are usually not full: unused slots sit before `_M_start` and after `_M_finish`. `push_front` and `push_back` write into those slots first. A new block is allocated only after that leftover room is gone.

The map is a normal contiguous array of pointers, one pointer per block. It also has empty slots on both ends, so a new 512-byte block can be prepended or appended without touching the old blocks. When the map has no empty pointer slot left, libstdc++ allocates a bigger pointer array and copies the addresses of existing blocks over. The blocks stay the same size, and the ints stay in those blocks.

That is why `int& x = dq[3];` still works after a `push_front`. `x` points at the int, and it did not move. An iterator is different: it also remembers "which entry in the map am I on?" After the list is replaced, that entry is gone, so the iterator is dead.

`operator[]` is still {% katex %}O(1){% endkatex %}. Index 200 with 128 ints per block is block 1, slot 72. Every 128 steps you leave a block and pick up the next pointer in the map, and `operator++` does that jump:

```cpp
_Self& operator++() {
    ++_M_cur;
    if (_M_cur == _M_last) {          // fell off this block
        _M_set_node(_M_node + 1);     // next pointer in _M_map
        _M_cur = _M_first;
    }
    return *this;
}
```

`_M_cur` is the current int. `_M_first` and `_M_last` are the ends of this block. `_M_node` is the map slot. When `_M_cur` hits `_M_last`, you switch to the next slot and start at the first int of that block. A middle `insert` is still linear. Everything from the insert point to the nearer end has to shift, one block at a time.

### 0-1 BFS

Shortest path, but every edge weight is 0 or 1.

You get a directed graph with {% katex %}n{% endkatex %} nodes and {% katex %}m{% endkatex %} edges, a start {% katex %}S{% endkatex %}, and a target {% katex %}T{% endkatex %}. Find the minimum cost of a path from {% katex %}S{% endkatex %} to {% katex %}T{% endkatex %}.

{% katex display %}
1 \le n, m \le 10^5
{% endkatex %}

I started with the BFS above. It treats every edge as one step, so it prefers a short walk even when that walk is expensive. In the GIF, {% katex %}S \rightarrow T{% endkatex %} is one edge and costs 1, and {% katex %}S \rightarrow A \rightarrow T{% endkatex %} is two edges and costs 0. The queue reaches {% katex %}T{% endkatex %} on the direct edge first. If we mark {% katex %}T{% endkatex %} visited at that moment, the free path through {% katex %}A{% endkatex %} never gets a chance.

So I switched to [Dijkstra](https://cp-algorithms.com/graph/dijkstra.html). The heap pops the smallest distance found so far, and the path through {% katex %}A{% endkatex %} wins. At {% katex %}n, m \le 10^5{% endkatex %} the extra {% katex %}\log n{% endkatex %} per pop is acceptable. It still felt like overkill: the heap keeps a full order, but every weight is 0 or 1. From the node you just popped you only care about two groups, neighbours that stay at this cost and neighbours that cost one more.

A deque can hold those two groups. `push_front` for a 0-edge, `push_back` for a 1-edge, `pop_front` as usual.

{% include image_full.html imageurl="/images/posts/stack-queue-deque/zero-one-bfs.gif" title="0-1 BFS on a four-node graph" caption="Green arrows cost 0, orange arrows cost 1. From S the direct edge marks T at cost 1 and goes to the back of the deque. Then A offers T a 0-edge. Cost drops to 0 and T is pushed on the front. After you pop T, the answer is 0." %}

```cpp
const int INF = 1e9;

int zero_one_bfs(int s, int t, const vector<vector<pair<int, int>>>& g) {
    vector<int> dist(g.size(), INF);
    deque<int> dq;
    dist[s] = 0;
    dq.push_back(s);
    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();
        for (auto [v, w] : g[u]) {       // w is 0 or 1
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v);
                else        dq.push_back(v);
            }
        }
    }
    return dist[t];
}
```

A node can enter the deque more than once. {% katex %}T{% endkatex %} first arrives at cost 1, then again at cost 0. The `if (dist[u] + w < dist[v])` check lets the better path replace the worse one.

Do not mark visited on the first enqueue. This setup is closer to Dijkstra: a later path can be cheaper, so you only keep the best `dist[v]` so far. Marking {% katex %}T{% endkatex %} on the first enqueue would freeze it at cost 1. A stack is also wrong here. It would follow a 0-edge immediately and leave other nodes in the same layer sitting in the container.

The practice list has a grid version: follow the painted arrow for free, step another way for cost 1.

## When they do not help

If you need the {% katex %}k{% endkatex %}-th element, a delete of an arbitrary value, or a predecessor, use a tree, an [ordered set](/Ordered-Set-data-structure-in-C++), or a heap.

If you need the smallest remaining key, use `priority_queue` or a set. Scanning a deque each time is slower.

If you only scan and index, use a `vector`. `deque` has {% katex %}O(1){% endkatex %} `[]`, but a long pass is still slower than a contiguous buffer. Reach for a deque when you `push_front`.

## Practice

- [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/): iterative inorder with a stack.
- [Number of Islands](https://leetcode.com/problems/number-of-islands/): DFS or BFS on a grid. Only the container changes.
- [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/): monotonic stack. Each index pushed once, popped once.
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/): BFS with a counted layer.
- [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/): BFS. The first time you dequeue the target is the hop distance.
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/): the deque animation above.
- [01 Matrix](https://leetcode.com/problems/01-matrix/): multi-source BFS. The queue starts with every zero.
- [Minimum Cost to Make at Least One Valid Path](https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/): 0-1 BFS. Cost 0 goes to the front, cost 1 to the back.
