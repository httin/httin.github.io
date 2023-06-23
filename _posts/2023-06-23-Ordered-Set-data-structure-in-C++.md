---
layout: post
title: "Ordered Set data structure in GNU C++"
description: "An advanced data structure in GNU C++ PBDS library"
date: 2023-06-23
feature_image: images/cpp-girl.jpg
tags: [GNU, datastructures]
---

Ordered Set là một cấu trúc dữ liệu policy-based của thư viện GNU C++. Giống như **std::set**, implementation của nó vẫn dựa trên Red Black Tree, mọi phần tử trong nó có tính thứ tự và nó cũng làm được tất cả những gì mà **std::set** làm được trong độ phức tạp thời gian *O(logN)*. Tuy nhiên, Orderer Set cung cấp thêm hai phương thức trong thời gian *O(logN)*
- **order_of_key (k)**: tính số phần tử nhỏ hơn **k**.
- **find_by_order(k)**: tìm phần tử thứ **k** trong tập hợp.

<!--more-->

Để sử dụng cấu trúc dữ liệu này, chúng ta cần xây dựng nó từ thư viện PBDS (policy-based data structures) 

```cpp
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

using namespace std;
using namespace __gnu_pbds;

template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
```

## Characteristics

As a naturally-occurring crystalline inorganic solid with an ordered structure, ice is considered a mineral.[citation needed] It possesses a regular crystalline structure based on the molecule of water, which consists of a single oxygen atom covalently bonded to two hydrogen atoms, or H-O-H. However, many of the physical properties of water and ice are controlled by the formation of hydrogen bonds between adjacent oxygen and hydrogen atoms; while it is a weak bond, it is nonetheless critical in controlling the structure of both water and ice.

> “ice contains no future , just the past, sealed away. As if they're alive, everything in the world is sealed up inside, clear and distinct. Ice can preserve all kinds of things that way- cleanly, clearly. That's the essence of ice, the role it plays.”
> <cite>― Haruki Murakami</cite>

An unusual property of ice frozen at atmospheric pressure is that the solid is approximately 8.3% less dense than liquid water. The density of ice is 0.9167 g/cm3 at 0 °C,[4] whereas water has a density of 0.9998 g/cm³ at the same temperature. Liquid water is densest, essentially 1.00 g/cm³, at 4 °C and becomes less dense as the water molecules begin to form the hexagonal crystals[5] of ice as the freezing point is reached. This is due to hydrogen bonding dominating the intermolecular forces, which results in a packing of molecules less compact in the solid. Density of ice increases slightly with decreasing temperature and has a value of 0.9340 g/cm³ at −180 °C (93 K).[6]

When water freezes, it increases in volume (about 9% for freshwater).[7] The effect of expansion during freezing can be dramatic, and ice expansion is a basic cause of freeze-thaw weathering of rock in nature and damage to building foundations and roadways from frost heaving. It is also a common cause of the flooding of houses when water pipes burst due to the pressure of expanding water when it freezes.

The result of this process is that ice _(in its most common form)_ floats on liquid water, which is an important feature in Earth's biosphere. It has been argued that without this property, natural bodies of water would freeze, in some cases permanently, from the bottom up,[8] resulting in a loss of bottom-dependent animal and plant life in fresh and sea water. Sufficiently thin ice sheets allow light to pass through while protecting the underside from short-term weather extremes such as wind chill. This creates a sheltered environment for bacterial and algal colonies. When sea water freezes, the ice is riddled with brine-filled channels which sustain sympagic organisms such as bacteria, algae, copepods and annelids, which in turn provide food for animals such as krill and specialised fish like the bald notothen, fed upon in turn by larger animals such as emperor penguins and minke whales.

When ice melts, it absorbs as much energy as it would take to heat an equivalent mass of water by 80 °C. During the melting process, the temperature remains constant at 0 °C. While melting, any energy added breaks the hydrogen bonds between ice (water) molecules. Energy becomes available to increase the thermal energy (temperature) only after enough hydrogen bonds are broken that the ice can be considered liquid water. The amount of energy consumed in breaking hydrogen bonds in the transition from ice to water is known as the heat of fusion.

As with water, ice absorbs light at the red end of the spectrum preferentially as the result of an overtone of an oxygen-hydrogen (O-H) bond stretch. Compared with water, this absorption is shifted toward slightly lower energies. Thus, ice appears blue, with a slightly greener tint than for liquid water. Since absorption is cumulative, the color effect intensifies with increasing thickness or if internal reflections cause the light to take a longer path through the ice.
