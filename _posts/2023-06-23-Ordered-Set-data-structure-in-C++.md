---
layout: post
title: "Ordered Set data structure in GNU C++"
description: "An advanced data structure in GNU C++ PBDS library"
date: 2023-06-23
feature_image: images/cpp-binary.jpg
katex: 1
categories: ["Data Structures and Algorithms"]
tags: [GNU, datastructures]
---

Ordered Set is a policy-based data structure from the GNU C++ library. Like **std::set**, its implementation is based on a Red-Black Tree: every element keeps a strict order, and it can do everything **std::set** can do, in *O(logN)* time complexity. However, sometimes we want to know the rank of an element, or find an element by its rank in the set. Ordered Set provides two extra methods for this, also in *O(logN)* time:
- **find_by_order(k)**: finds the element with the **k**-th largest rank in the set (0-indexed).
- **order_of_key(k)**: returns the number of elements smaller than **k**.


<!--more-->
## Introduction
To use this data structure, we need to build it from the PBDS (policy-based data structures) library

{% highlight cpp %}
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

using namespace std;
using namespace __gnu_pbds;

template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
{% endhighlight %}

Alternatively, you can use `#include <ext/pb_ds/detail/standard_policies.hpp>`{:.cpp} instead of including the two headers `<ext/pb_ds/assoc_container.hpp>` and `<ext/pb_ds/tree_policy.hpp>` separately, since they are already included inside `<ext/pb_ds/detail/standard_policies.hpp>`.

For example,
```cpp
ordered_set T;
T.insert(1);
T.insert(2);
T.insert(4);
T.insert(8);
T.insert(16);

cout<<*T.find_by_order(1)<<endl; // 2
cout<<*T.find_by_order(2)<<endl; // 4
cout<<*T.find_by_order(4)<<endl; // 16
cout<<(std::end(T)==T.find_by_order(6))<<endl; // true

cout<<T.order_of_key(-5)<<endl;  // 0
cout<<T.order_of_key(1)<<endl;   // 0
cout<<T.order_of_key(3)<<endl;   // 2
cout<<T.order_of_key(4)<<endl;   // 2
cout<<T.order_of_key(400)<<endl; // 5
```

Another example is available at https://opensource.apple.com/source/llvmgcc42/llvmgcc42-2336.9/libstdc++-v3/testsuite/ext/pb_ds/example/tree_order_statistics.cc

## Deep Dive
In it, the tree-based container is defined as follows
```cpp
  /**
   *  A tree-based container.
   *
   *  @tparam Key 	 	Key type.
   *  @tparam Mapped 	 	Map type.
   *  @tparam Cmp_Fn	 	Comparison functor.
   *  @tparam Tag 	 	Instantiating data structure type,
   *                            see container_tag.
   *  @tparam Node_Update 	Updates tree internal-nodes,
   *                            restores invariants when invalidated.
   *                     XXX See design::tree-based-containers::node invariants.
   *  @tparam _Alloc 	 	Allocator type.
   *
   *  Base tag choices are: ov_tree_tag, rb_tree_tag, splay_tree_tag.
   *
   *  Base is basic_branch.
   */
  template<
    typename Key,
    typename Mapped,
    typename Cmp_Fn = std::less<Key>,
    typename Tag = rb_tree_tag,
    template<typename Node_CItr, typename Node_Itr, typename Cmp_Fn_, typename _Alloc_> class Node_Update = null_node_update,
    typename _Alloc = std::allocator<char> 
  > class tree : public PB_DS_TREE_BASE
  {
  ...
```

In this template, if we instantiate **tree** with only the first two parameters, we get **std::map**. If we set *Mapped* to *null_type*, we get **std::set**. Here is a closer look at the other type parameters.

<code class="codeforces" style="color:#800; font-family:Consolas;">Tag</code> -- defines the tree structure. The STL provides 3 base classes: `rb_tree_tag` (Red Black Tree), `splay_tree_tag` (Splay Tree) and `ov_tree_tag` (ordered-vector tree). In competitive programming, we usually use the Red Black Tree, because the Splay Tree and OV Tree have operations that run in linear time.

<code class="codeforces" style="color:#800; font-family:Consolas;">Node_Update</code> -- defines the update policy for the nodes in the tree. By default, its value is `null_node_update`, which does not store any extra information in the nodes. `tree_order_statistics_node_update`, on the other hand, is a node update policy from the **C++** `<ext/pb_ds/tree_policy.hpp>` header. It stores the extra information the tree needs in each node, which costs a small amount of performance.

Finally, here is a good way to declare this tree structure in **C++**

{% highlight cpp %}
template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
{% endhighlight %}

If we use a **Mapped** type as the second parameter, we get the **Ordered Map** data structure!

## Problems
1. [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/)
2. Sliding Median

> You are given an array of `n` integers. Your task is to calculate the median of each window of `k` elements, from left to right. The median is the middle element when the elements are sorted. If the number of elements is even, there are two possible medians and we assume that the median is the smaller of them.

**Input**
The first input line contains two integers `n` and `k`: the number of elements and the size of the window.
Then there are `n` integers {% katex %}x_1,x_2,…,x_n{% endkatex %}: the contents of the array.

**Output**
Print `n−k+1` values: the medians.

**Constraints**

{% katex %}
1 \le k \le n \le 2*10^5
{% endkatex %}

{% katex %}
1\le x_i\le 109
{% endkatex %}

**Example**
Input:
```
8 3
2 4 3 5 8 1 2 1
```
Output:
```
3 4 5 5 2 1
```