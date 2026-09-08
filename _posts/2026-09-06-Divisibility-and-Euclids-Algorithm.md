---
layout: post
title: "Divisibility and Euclidean Algorithm"
description: "Common multiples, common divisors and the remainder loop."
date: 2026-09-06
thumbnail: /images/posts/divisibility/poster.jpg
katex: 1
categories: ["Math"]
tags: [number-theory, algorithms]
---

<!--more-->

## Least common multiple

Write {% katex %}a_1, a_2, \ldots, a_n{% endkatex %} for a finite list of nonzero integers. An integer that is divisible by every {% katex %}a_i{% endkatex %} is a common multiple of the list.

The list has infinitely many positive common multiples. One of them is {% katex %}|a_1 a_2 \cdots a_n|{% endkatex %}. A nonempty set of positive integers has a least element. That least positive common multiple is the least common multiple, written {% katex %}[a_1, a_2, \ldots, a_n]{% endkatex %}.

**Theorem 1.** Every common multiple of those integers is divisible by their least common multiple.

**Proof.** Write {% katex %}m = [a_1, \ldots, a_n]{% endkatex %} and let {% katex %}M{% endkatex %} be any common multiple. Divide:

{% katex display %}
M = qm + r, \qquad 0 \le r < m.
{% endkatex %}

Then {% katex %}r = M - qm{% endkatex %}. Both {% katex %}M{% endkatex %} and {% katex %}m{% endkatex %} are common multiples, so {% katex %}r{% endkatex %} is a common multiple. If {% katex %}r > 0{% endkatex %}, then {% katex %}r{% endkatex %} is a positive common multiple smaller than {% katex %}m{% endkatex %}, which is impossible. So {% katex %}r = 0{% endkatex %} and {% katex %}m \mid M{% endkatex %}. {% katex %}\blacksquare{% endkatex %}

## Greatest common divisor

Let {% katex %}S = \{a_1, a_2, \ldots\}{% endkatex %} be a set of integers, finite or infinite, with at least one nonzero entry, say {% katex %}a_0{% endkatex %}. An integer {% katex %}d{% endkatex %} that divides every element of {% katex %}S{% endkatex %} is a common divisor of {% katex %}S{% endkatex %}.

Any such {% katex %}d{% endkatex %} divides {% katex %}a_0{% endkatex %}, so {% katex %}|d| \le |a_0|{% endkatex %}. Only finitely many integers satisfy that bound, so {% katex %}S{% endkatex %} has finitely many common divisors, and a greatest one exists. Call it {% katex %}d_S{% endkatex %}, the greatest common divisor of {% katex %}S{% endkatex %}, written {% katex %}(a_1, a_2, \ldots, a_n){% endkatex %}.

**Theorem 2.** Every other common divisor of the integers in {% katex %}S{% endkatex %} divides {% katex %}d_S{% endkatex %}.

**Proof.** Let {% katex %}d{% endkatex %} be any common divisor, and set {% katex %}N = [d, d_S]{% endkatex %}. Take any {% katex %}a \in S{% endkatex %}. Then {% katex %}d \mid a{% endkatex %} and {% katex %}d_S \mid a{% endkatex %}, so {% katex %}a{% endkatex %} is a common multiple of {% katex %}d{% endkatex %} and {% katex %}d_S{% endkatex %}. Theorem 1 gives {% katex %}N \mid a{% endkatex %}. Thus {% katex %}N{% endkatex %} is also a common divisor of {% katex %}S{% endkatex %}.

{% katex %}d_S{% endkatex %} is the greatest common divisor, so {% katex %}N \le d_S{% endkatex %}. But {% katex %}N{% endkatex %} is the least common multiple of {% katex %}d{% endkatex %} and {% katex %}d_S{% endkatex %}, so {% katex %}N \ge d_S{% endkatex %}. Therefore {% katex %}N = d_S{% endkatex %}, and {% katex %}d \mid N{% endkatex %} is equivalent to {% katex %}d \mid d_S{% endkatex %}. {% katex %}\blacksquare{% endkatex %}

### Euclidean algorithm

The Euclidean algorithm is also called the division algorithm, Euclid's algorithm, or the continued fraction algorithm.

**Claim.** If {% katex %}b \neq 0{% endkatex %} and {% katex %}a = qb + r{% endkatex %} with {% katex %}0 \le r < |b|{% endkatex %}, then {% katex %}(a,b) = (b,r){% endkatex %}. If {% katex %}b = 0{% endkatex %}, then {% katex %}(a,0) = |a|{% endkatex %}.

**Proof.** If {% katex %}d \mid a{% endkatex %} and {% katex %}d \mid b{% endkatex %}, then {% katex %}d \mid r{% endkatex %} because {% katex %}r = a - qb{% endkatex %}. If {% katex %}d \mid b{% endkatex %} and {% katex %}d \mid r{% endkatex %}, then {% katex %}d \mid a{% endkatex %}. The pairs {% katex %}(a,b){% endkatex %} and {% katex %}(b,r){% endkatex %} have the same common divisors. Theorem 2 says they have the same greatest one. If {% katex %}b = 0{% endkatex %}, every divisor of {% katex %}a{% endkatex %} is a common divisor of {% katex %}(a,0){% endkatex %}, so the greatest is {% katex %}|a|{% endkatex %}. {% katex %}\blacksquare{% endkatex %}

The algorithm is the recurrence until the remainder is {% katex %}0{% endkatex %}.

1. Replace {% katex %}(a,b){% endkatex %} by {% katex %}(|a|,|b|){% endkatex %}. If {% katex %}b > a{% endkatex %}, swap.
2. If {% katex %}b = 0{% endkatex %}, return {% katex %}a{% endkatex %}.
3. Write {% katex %}a = qb + r{% endkatex %} with {% katex %}0 \le r < b{% endkatex %}.
4. Replace {% katex %}(a,b){% endkatex %} by {% katex %}(b,r){% endkatex %} and go to step 2.

```cpp
long long gcd(long long a, long long b) {
    a = llabs(a);
    b = llabs(b);
    while (b) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}
```

This implementation is equivalent to C++17 `std::gcd`, with {% katex %}(a,0) = |a|{% endkatex %}. For more than two integers, use {% katex %}
(a,b,c) = ((a,b),c){% endkatex %} which has been proved in Theorem 5.

**Example.** Take {% katex %}(483, 210){% endkatex %}, we have

{% katex display %}
\begin{aligned}
483 &= 2 \cdot 210 + 63, \\
210 &= 3 \cdot 63 + 21, \\
63 &= 3 \cdot 21 + 0.
\end{aligned}
{% endkatex %}

The claim at each line gives {% katex %}(483,210) = (210,63) = (63,21) = (21,0) = 21{% endkatex %}.

{% include image_full.html imageurl="/images/posts/divisibility/euclidean-algorithm.gif" title="Euclidean algorithm" caption="illustrate euclidean algorithm using geometry" %}

Each remainder is a natural number strictly smaller than the previous {% katex %}b{% endkatex %}, so the process stops after finite steps. The value returned is {% katex %}(a,b){% endkatex %} by the claim at every step.

A step writes {% katex %}a = qb + r{% endkatex %}. If {% katex %}q \ge 2{% endkatex %}, then {% katex %}a \ge 2b{% endkatex %}, so both entries of the next pair {% katex %}(b,r){% endkatex %} are at most {% katex %}a/2{% endkatex %}. The slowest drop is {% katex %}q = 1{% endkatex %} whenever {% katex %}b < a < 2b{% endkatex %}: then {% katex %}r = a - b{% endkatex %} and the remainders obey {% katex %}r_{i-1} = r_i + r_{i+1}{% endkatex %}. That is the Fibonacci recurrence run backwards. Write {% katex %}F_1 = 1{% endkatex %}, {% katex %}F_2 = 1{% endkatex %}, {% katex %}F_k = F_{k-1} + F_{k-2}{% endkatex %}. The last quotient is at least {% katex %}2{% endkatex %}, so the smallest pair that needs {% katex %}n{% endkatex %} divisions is {% katex %}(F_{n+2}, F_{n+1}){% endkatex %}. For example {% katex %}(377, 233) = (F_{14}, F_{13}){% endkatex %} uses twelve divisions, while {% katex %}(483, 210){% endkatex %} uses three. The recurrence {% katex %}F_k = F_{k-1} + F_{k-2}{% endkatex %} has characteristic equation {% katex %}x^2 - x - 1 = 0{% endkatex %}. The roots are {% katex %}\varphi = (1+\sqrt{5})/2{% endkatex %} and {% katex %}\hat{\varphi} = (1-\sqrt{5})/2{% endkatex %}. The solution is

{% katex display %}
F_n = \frac{\varphi^n - \hat{\varphi}^n}{\sqrt{5}}.
{% endkatex %}

Because {% katex %}|\hat{\varphi}| < 1{% endkatex %}, the second term vanishes as {% katex %}n{% endkatex %} grows, so {% katex %}F_n{% endkatex %} grows like {% katex %}\varphi^n{% endkatex %}. Even that worst case is therefore {% katex %}O(\log \min(a,b)){% endkatex %}.

## Coprime numbers

**Definition.** Two integers {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %} are coprime if {% katex %}(a,b) = 1{% endkatex %}.

Take any integers {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %}, and write {% katex %}d = (a,b){% endkatex %}. Set {% katex %}a_1 = a/d{% endkatex %} and {% katex %}b_1 = b/d{% endkatex %}. Suppose {% katex %}a_1{% endkatex %} and {% katex %}b_1{% endkatex %} are not coprime, that is {% katex %}(a_1,b_1) = d_1 > 1{% endkatex %}. Then {% katex %}a_2 = a_1/d_1{% endkatex %} and {% katex %}b_2 = b_1/d_1{% endkatex %} are integers, so {% katex %} a = d\, d_1\, a_2, \quad b = d\, d_1\, b_2. {% endkatex %}

Thus {% katex %}d\, d_1{% endkatex %} is a common divisor of {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %}. But {% katex %}d{% endkatex %} is the greatest one, so {% katex %}d\, d_1 \le d{% endkatex %}, hence {% katex %}d_1 \le 1{% endkatex %}. That contradicts {% katex %}d_1 > 1{% endkatex %}. Dividing {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %} by {% katex %}(a,b){% endkatex %} therefore yields a coprime pair. The same reduction works for a finite list.

**Theorem 3.** If {% katex %}d = (a_1, a_2, \ldots, a_n){% endkatex %} and {% katex %}b_i = a_i/d{% endkatex %}, then {% katex %}(b_1, b_2, \ldots, b_n) = 1{% endkatex %}.

**Proof.** Suppose {% katex %}(b_1, \ldots, b_n) = d_1 > 1{% endkatex %}. Each {% katex %}b_i/d_1{% endkatex %} is an integer, so {% katex %}a_i = d\, d_1\, (b_i/d_1){% endkatex %}. Then {% katex %}d\, d_1{% endkatex %} is a common divisor of {% katex %}a_1, \ldots, a_n{% endkatex %}. The greatest common divisor is {% katex %}d{% endkatex %}, so {% katex %}d\, d_1 \le d{% endkatex %} and {% katex %}d_1 \le 1{% endkatex %}, a contradiction. {% katex %}\blacksquare{% endkatex %}

A divisor of a coprime pair cannot share a factor with the other entry. That is the next piece.

**Lemma.** If {% katex %}(a,b) = 1{% endkatex %} and {% katex %}c \mid a{% endkatex %}, then {% katex %}(c,b) = 1{% endkatex %}.

**Proof.** Let {% katex %}d = (c,b){% endkatex %}. Then {% katex %}d \mid c{% endkatex %} and {% katex %}d \mid b{% endkatex %}. Since {% katex %}c \mid a{% endkatex %}, we also have {% katex %}d \mid a{% endkatex %}. So {% katex %}d{% endkatex %} is a common divisor of {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %}. Theorem 2 gives {% katex %}d \mid (a,b){% endkatex %}, hence {% katex %}d \mid 1{% endkatex %} and {% katex %}d = 1{% endkatex %}. {% katex %}\blacksquare{% endkatex %}

## GCD and LCM

**Theorem 4.** If {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %} are natural numbers, then {% katex %}ab = (a,b)\,[a,b]{% endkatex %}.

**Proof.** Write {% katex %}d = (a,b){% endkatex %} and {% katex %}m = [a,b]{% endkatex %}. The product {% katex %}ab{% endkatex %} is a common multiple of {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %}, so Theorem 1 gives {% katex %}m \mid ab{% endkatex %}. Thus {% katex %}ab/m{% endkatex %} is a natural number.

Since {% katex %}a \mid m{% endkatex %} and {% katex %}b \mid m{% endkatex %}, both {% katex %}m/a{% endkatex %} and {% katex %}m/b{% endkatex %} are natural numbers, and

{% katex display %}
\frac{a}{ab/m} = \frac{m}{b}, \qquad \frac{b}{ab/m} = \frac{m}{a}.
{% endkatex %}

So {% katex %}ab/m{% endkatex %} divides both {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %}. It is a common divisor. Theorem 2 gives {% katex %}ab/m \mid d{% endkatex %}.

The other way: {% katex %}ab/d{% endkatex %} is a common multiple of {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %}, because {% katex %}(ab/d)/a = b/d{% endkatex %} and {% katex %}(ab/d)/b = a/d{% endkatex %} are natural numbers. Theorem 1 gives {% katex %}m \mid ab/d{% endkatex %}, so {% katex %}d \mid ab/m{% endkatex %}.

Two natural numbers that divide each other are equal. Hence {% katex %}ab/m = d{% endkatex %}, that is {% katex %}ab = (a,b)\,[a,b]{% endkatex %}. {% katex %}\blacksquare{% endkatex %}

Theorem 3 rewrites Theorem 4. Set {% katex %}d = (a,b){% endkatex %}, {% katex %}a = d a_1{% endkatex %}, {% katex %}b = d b_1{% endkatex %}, so {% katex %}(a_1,b_1) = 1{% endkatex %}. Then

{% katex display %}
ab = (d a_1)(d b_1) = d \cdot (d a_1 b_1).
{% endkatex %}

Theorem 4 says the second factor is {% katex %}[a,b]{% endkatex %}. Hence {% katex %}[a,b] = d\, a_1 b_1 = a/d \cdot b{% endkatex %}. A contest program that asks for {% katex %}[a,b]{% endkatex %} computes {% katex %}d{% endkatex %} by the Euclidean algorithm, then multiplies {% katex %}a/d{% endkatex %} by {% katex %}b{% endkatex %}.

If {% katex %}a{% endkatex %} and {% katex %}b{% endkatex %} are coprime, then {% katex %}d = (a,b) = 1{% endkatex %} and Theorem 4 becomes {% katex %}ab = [a,b]{% endkatex %}.

**Corollary.** The least common multiple of two coprime natural numbers is their product.

The n-ary notations {% katex %}(a_1,\ldots,a_n){% endkatex %} and {% katex %}[a_1,\ldots,a_n]{% endkatex %} were defined as a greatest common divisor and a least common multiple of the whole list. They reduce to the binary case one entry at a time.

**Theorem 5.** If {% katex %}a_1,\ldots,a_{n+1}{% endkatex %} are nonzero integers, then

{% katex display %}
(a_1,a_2,\ldots,a_{n+1}) = ((a_1,a_2,\ldots,a_n),a_{n+1})
{% endkatex %}

and

{% katex display %}
[a_1,a_2,\ldots,a_{n+1}] = [[a_1,a_2,\ldots,a_n],a_{n+1}].
{% endkatex %}

**Proof.** Write {% katex %}d = (a_1,\ldots,a_n){% endkatex %} and {% katex %}D = (a_1,\ldots,a_{n+1}){% endkatex %}, and set {% katex %}d' = (d,a_{n+1}){% endkatex %}.

Then {% katex %}d' \mid d{% endkatex %} and {% katex %}d{% endkatex %} divides each of {% katex %}a_1,\ldots,a_n{% endkatex %}, so {% katex %}d'{% endkatex %} divides each of those. Also {% katex %}d' \mid a_{n+1}{% endkatex %}. Thus {% katex %}d'{% endkatex %} is a common divisor of {% katex %}a_1,\ldots,a_{n+1}{% endkatex %}. Theorem 2 gives {% katex %}d' \mid D{% endkatex %}.

The other way: {% katex %}D{% endkatex %} divides each of {% katex %}a_1,\ldots,a_{n+1}{% endkatex %}, so {% katex %}D{% endkatex %} is a common divisor of {% katex %}a_1,\ldots,a_n{% endkatex %}. Theorem 2 gives {% katex %}D \mid d{% endkatex %}. Also {% katex %}D \mid a_{n+1}{% endkatex %}. Thus {% katex %}D{% endkatex %} is a common divisor of {% katex %}d{% endkatex %} and {% katex %}a_{n+1}{% endkatex %}, so Theorem 2 gives {% katex %}D \mid d'{% endkatex %}.

Two natural numbers that divide each other are equal. Hence {% katex %}D = d'{% endkatex %}.

For the second identity, write {% katex %}m = [a_1,\ldots,a_n]{% endkatex %} and {% katex %}M = [a_1,\ldots,a_{n+1}]{% endkatex %}, and set {% katex %}m' = [m,a_{n+1}]{% endkatex %}.

Then {% katex %}m \mid m'{% endkatex %} and each {% katex %}a_i \mid m{% endkatex %} for {% katex %}i \le n{% endkatex %}, so each {% katex %}a_i \mid m'{% endkatex %}. Also {% katex %}a_{n+1} \mid m'{% endkatex %}. Thus {% katex %}m'{% endkatex %} is a common multiple of {% katex %}a_1,\ldots,a_{n+1}{% endkatex %}. Theorem 1 gives {% katex %}M \mid m'{% endkatex %}.

The other way: {% katex %}M{% endkatex %} is a common multiple of {% katex %}a_1,\ldots,a_{n+1}{% endkatex %}, so {% katex %}M{% endkatex %} is a common multiple of {% katex %}a_1,\ldots,a_n{% endkatex %}. Theorem 1 gives {% katex %}m \mid M{% endkatex %}. Also {% katex %}a_{n+1} \mid M{% endkatex %}. Thus {% katex %}M{% endkatex %} is a common multiple of {% katex %}m{% endkatex %} and {% katex %}a_{n+1}{% endkatex %}, so Theorem 1 gives {% katex %}m' \mid M{% endkatex %}.

Hence {% katex %}M = m'{% endkatex %}. {% katex %}\blacksquare{% endkatex %}

## Practice

- [Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/).
- [Common Divisors](https://cses.fi/problemset/task/1081).
