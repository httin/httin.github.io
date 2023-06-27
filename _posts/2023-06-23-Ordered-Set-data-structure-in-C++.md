---
layout: post
title: "Ordered Set data structure in GNU C++"
description: "An advanced data structure in GNU C++ PBDS library"
date: 2023-06-23
feature_image: images/cpp-binary.jpg
tags: [GNU, datastructures]
---

Ordered Set là một cấu trúc dữ liệu policy-based của thư viện GNU C++. Giống như **std::set**, implementation của nó vẫn dựa trên Red Black Tree, mọi phần tử trong nó có tính thứ tự và nó cũng làm được tất cả những gì mà **std::set** làm được trong độ phức tạp thời gian *O(logN)*. Tuy nhiên, trong một số trường hợp chúng ta muốn biết thứ tự của một phần tử hoặc là tìm phần tử khi biết trước thứ tự của nó trong tập hợp, Ordered Set cung cấp thêm hai phương thức trong thời gian *O(logN)*
- **find_by_order(k)**: tìm phần tử lớn thứ **k** trong tập hợp (tính từ **0**).
- **order_of_key(k)**: số phần tử nhỏ hơn **k**.


<!--more-->
## Introduction
Để sử dụng cấu trúc dữ liệu này, chúng ta cần xây dựng nó từ thư viện PBDS (policy-based data structures) 

{% highlight cpp %}
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

using namespace std;
using namespace __gnu_pbds;

template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
{% endhighlight %}

Ngoài ra, ta có thể sử dụng `#include <ext/pb_ds/detail/standard_policies.hpp>`{:.cpp} thay cho việc include hai thư viện `<ext/pb_ds/assoc_container.hpp>` và `<ext/pb_ds/tree_policy.hpp>` vì chúng đã có trong `<ext/pb_ds/detail/standard_policies.hpp>`.

Ví dụ,
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

Một ví dụ khác ở https://opensource.apple.com/source/llvmgcc42/llvmgcc42-2336.9/libstdc++-v3/testsuite/ext/pb_ds/example/tree_order_statistics.cc

## Deep Dive
Trong đó, cấu trúc tree-based được định nghĩa như sau
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

Trong template này, nếu chúng ta khởi tạo **tree** với hai tham số đầu, ta sẽ có **std::map**, nếu set *Mapped* là *null_type*, ta có **std::set**. Hiểu thêm về các typename khác

<code class="codeforces" style="color:#800; font-family:Consolas;">Tag</code> -- định nghĩa cấu trúc cây. STL cung cấp 3 base classes là `rb_tree_tag` (Red Black Tree), `splay_tree_tag` (Splay Tree) and `ov_tree_tag` (ordered-vector tree). Trong competitive programming, chúng ta thường sử dụng Red Black Tree vì Splay Tree và OV Tree sử dụng các operations trong thời gian tuyến tính.

<code class="codeforces" style="color:#800; font-family:Consolas;">Node_Update</code> -- định nghĩa update policy cho các nodes trong cây. Mặc định, gái trị mặc định của nó là `null_node_update`, nó sẽ không lưu thêm thông tin vào các đỉnh. Còn `tree_order_statistics_node_update` là một node update policy có trong thư viện `<ext/pb_ds/tree_policy.hpp>` của **C++**, sẽ lưu thêm thông tin cần thiết vào các đỉnh, vì vậy làm giảm performance của nó đi một ít.

Cuối cùng, chúng ta có một cách cài đặt khá tốt cho cấu trúc cây của **C++**

{% highlight cpp %}
template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
{% endhighlight %}

Nếu chúng ta dùng một **Mapped** type ở tham số thứ hai, ta sẽ có CTDL **Ordered Map**!

## Problems
1. [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/)
2. Sliding Median

> You are given an array of `n` integers. Your task is to calculate the median of each window of `k` elements, from left to right. The median is the middle element when the elements are sorted. If the number of elements is even, there are two possible medians and we assume that the median is the smaller of them.

**Input**
{% katex %}
The first input line contains two integers `n` and `k`: the number of elements and the size of the window.
Then there are `n` integers x_1,x_2,…,x_n: the contents of the array.

**Output**
Print `n−k+1` values: the medians.

**Constraints**
1\le k\le n \le 2*10^5
1\le x_i\le 109

**Example**
Input:
8 3
2 4 3 5 8 1 2 1
Output:
3 4 5 5 2 1
{% endkatex %}
