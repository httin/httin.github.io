---
layout: post
title: "Ordered Set data structure in GNU C++"
description: "An advanced data structure in GNU C++ PBDS library"
date: 2023-06-23
feature_image: images/cpp-binary.jpg
tags: [GNU, datastructures]
---

Ordered Set là một cấu trúc dữ liệu policy-based của thư viện GNU C++. Giống như **std::set**, implementation của nó vẫn dựa trên Red Black Tree, mọi phần tử trong nó có tính thứ tự và nó cũng làm được tất cả những gì mà **std::set** làm được trong độ phức tạp thời gian *O(logN)*. Tuy nhiên, trong một số trường hợp chúng ta muốn biết thứ tự của một phần tử hoặc là tìm phần tử khi biết trước thứ tự của nó trong tập hợp, Ordered Set cung cấp thêm hai phương thức trong thời gian *O(logN)*
- **find_by_order(k)**: tìm phần tử có thứ tự là **k** trong tập hợp.
- **order_of_key(k)**: số phần tử nhỏ hơn **k**, hoặc thứ tự của **k**.


<!--more-->

Để sử dụng cấu trúc dữ liệu này, chúng ta cần xây dựng nó từ thư viện PBDS (policy-based data structures) 

{% highlight ruby %}
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

using namespace std;
using namespace __gnu_pbds;

template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
{% endhighlight %}

Ngoài ra, ta có thể sử dụng `#include <ext/pb_ds/detail/standard_policies.hpp>`{:.cpp} thay cho việc include hai thư viện `<ext/pb_ds/assoc_container.hpp>` và `<ext/pb_ds/tree_policy.hpp>` vì chúng đã có trong `<ext/pb_ds/detail/standard_policies.hpp>`

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

<code class="code">Tag</code> -- định nghĩa cấu trúc cây. STL cung cấp 3 base classes là `rb_tree_tag` (red-black tree), `splay_tree_tag` (splay tree) and `ov_tree_tag` (ordered-vector tree

## Characteristics

As a naturally-occurring crystalline inorganic solid with an ordered structure, ice is considered a mineral.[citation needed] It possesses a regular crystalline structure based on the molecule of water, which consists of a single oxygen atom covalently bonded to two hydrogen atoms, or H-O-H. However, many of the physical properties of water and ice are controlled by the formation of hydrogen bonds between adjacent oxygen and hydrogen atoms; while it is a weak bond, it is nonetheless critical in controlling the structure of both water and ice.

> “ice contains no future , just the past, sealed away. As if they're alive, everything in the world is sealed up inside, clear and distinct. Ice can preserve all kinds of things that way- cleanly, clearly. That's the essence of ice, the role it plays.”
> <cite>― Haruki Murakami</cite>

An unusual property of ice frozen at atmospheric pressure is that the solid is approximately 8.3% less dense than liquid water. The density of ice is 0.9167 g/cm3 at 0 °C,[4] whereas water has a density of 0.9998 g/cm³ at the same temperature. Liquid water is densest, essentially 1.00 g/cm³, at 4 °C and becomes less dense as the water molecules begin to form the hexagonal crystals[5] of ice as the freezing point is reached. This is due to hydrogen bonding dominating the intermolecular forces, which results in a packing of molecules less compact in the solid. Density of ice increases slightly with decreasing temperature and has a value of 0.9340 g/cm³ at −180 °C (93 K).[6]

When water freezes, it increases in volume (about 9% for freshwater).[7] The effect of expansion during freezing can be dramatic, and ice expansion is a basic cause of freeze-thaw weathering of rock in nature and damage to building foundations and roadways from frost heaving. It is also a common cause of the flooding of houses when water pipes burst due to the pressure of expanding water when it freezes.
