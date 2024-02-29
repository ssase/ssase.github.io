---
layout: post
title: "The Essence of Regular Expression"
date: 2024-02-23 16:44:06 +0800
published: true
categories: [Finite Automaton]
tags: [regular expression]
# The categories of each post are designed to contain up to two elements, and the number of elements in tags can be zero to infinity. 
# TAG names should always be lowercase
author: max
toc: true
comments: false
math: true
mermaid: true
# Mermaid is a great diagram generation tool
---


## Introduction to Regular Expression

### What is Regualar Expression

As a developer, we may be more or less familiar with **regular expression**(also known as **regex** or **regexp**). It is a way to decribe a string pattern with which we can tell whether a string is needed or locate a special piece of text in an article.

### Why Regular Expression

Assuming you are told to delelop a website's login page, users can enter their email to login, and we all know that an email is like `username@companyname.urlsuffix`, but how to describe it? An easy way is to use **regular expression** to describe the email like this `[\w.%+-]+@[\w.-]+\.[a-zA-Z]+`.

### What's in Regular Expression

Let's take an easiest **mathematical expression** `1 + 1` as an example, we use two **numbers** and one **mathematical operation** to form a **mathematical expression**, and the result is still a **number**.

Like the **mathematical expression**, **regular expression** has similar components, we call them **regular language** and **regualar operation**.

Before to answer what is **regular language** and **regualar operation**, we need to introduce a new model called **Finite Automaton**.

## Finite Automaton

> "A **finite automaton**, **finite-state machine** (FSM) or **finite-state automaton** (FSA, plural: automata), or simply a **state machine**, is a mathematical model of computation". -Wikipedia

### A Simple Finite Automaton

Assuming that you are told to design an automatic door controller with 2 states(*OPEN* and *CLOSED*), it can receive 4 signals(*FRONT* standing for there's someone in the front of the door and *REAR* standing for there's someone in the rear of the door, *BOTH* standing for there's someone in front and rear of the door and *NEITHER* standing for there's noone in front or rear of the door). Then we can figure out an diagram as below:

```mermaid
stateDiagram
    direction LR
    [*] --> CLOSED
    CLOSED --> OPEN : FRONT, REAR, BOTH
    OPEN --> CLOSED : NEITHER
    CLOSED --> CLOSED : NEITHER
    OPEN --> OPEN : FRONT, REAR, BOTH
```

And we just get a simple finite automaton.

### Deterministic Finite Automaton (DFA)

Here is a more abstract diagram.

```mermaid
graph LR
    q(( )) --> q1((q1))
    q1 --1--> q1
    q1 --0--> q2(((q2)))
    q2 --1--> q1
    q2 --0--> q2
```

$M_1$ above is a **state diagram** which has 2 states called $q_1$ and $q_2$. $q_1$ is a **start state** pointed by a single pointer, $q_2$ is an **accept state** with concentric circles. A pointer pointing from one state to another is called **transition**.

When $M_1$ receives a string assuming it's `1010`, then it runs as steps below:
1. Starts at $q_1$.
2. Reads 1, stays $q_1$.
3. Reads 0, transits to $q_2$.
4. Reads 1, transits to $q_1$.
5. Reads 0, transits to $q_2$.
6. Ends at $q_2$, since $q_2$ is an **accept state**, this string is accepted by $M_1$.

By testing a few strings with $M_1$, we can find that $M_1$ accepts strings which end with 0.

A finite automaton like $M_1$ is called **Deterministic Finite Automaton**(DFA).

Now we can define *DFA* as a 5-tuple, $(Q, \Sigma, \delta, q_0, F)$, and:
1. $Q$ is a finite set called **state set**.
2. $\Sigma$ is a finite set called **alphabet**.
3. $\delta: Q \times \Sigma \rightarrow Q$ is a **transition function**.
4. $q_0 \in Q$ is a **start state**.
5. $F \subseteq Q$ is a **set of accept states**.

So, $M_1$ can be defined as $(Q, \Sigma, \delta, q_0, F)$, and:
1. $Q = \{q_1, q_2\}$
2. $\Sigma = \{0, 1\}$
3. $\delta$ can be described as

||0|1|
|---|---|---|
|$q_1$|$q_2$|$q_1$|
|$q_2$|$q_2$|$q_1$|

4. $q_1$ is a **start state**
5. $F = \{q_2\}$

### Nondeterministic Finite Automaton (NFA)

Here is a simple *NFA* $N_1$:

```mermaid
graph LR
    q(( )) --> q1((q1))
    q1 --0, 1--> q1
    q1 --1, ε--> q2(((q2)))
```

As we can see, there are 2 pointers starting from $q_1$, which means when the NFA's state is $q_1$, meanwhile if it receives `1`, the result is 2 different states. And there is an $\varepsilon$ on the pointer starting from $q_1$ to $q_2$, which means the *NFA* can receive an empty char so that it can transit from $q_1$ to $q_2$ without consuming any chars in string. Besides, there is also no pointer starting from a state like $q_2$.

Since the *NFA* might have diffenent states, it assumes all of the states can lead to the right result, and it will split into the number of the states, each automaton will excuse the rest part of the string.

Let's take a string `010` as an example. Its excusing path is illustrated as below:

```mermaid
graph
    a(( )) --> a1((N1-q1-0))
    a1 --0--> a2((N1-q1-1))
    a1 --ε--> a3((N2-q2-0))
    a2 --1--> a4((N1-q1-2))
    a2 --ε--> a6((N3-q2-1))
    a2 --1--> a5((N4-q2-2))
    a4 --0--> a7((N1-q1-3))
    a4 --ε--> a8((N5-q2-2))
    a7 --ε--> a9(((N1-q2-4)))
```

> *Nx* means the name of *NFA*, *qx* means the current state of the *NFA*, and the number at the right side of the second '-' means how many numbers in string it has consumed(including the *NFA* it splited from).

The *NFA* *N1* starts from *q1*, because it can receive an $\varepsilon$ at *q1*, it will split a new *NFA* *N2*. After *N1* consumes a `0`, its state is still *q1*, so it can split a new *NFA* *N3* again by receiving an $\varepsilon$, and at this time, since the next number is `1`, it will split a new *NFA* *N4*. Keeping folliwing *N1*, now it is at *N1-q1-2*, like previous examples, *N1* will split a new *NFA* *N5* and comsume `0` from string. But though *N1*'s state is *q1*, and it will receive another $\varepsilon$, for no more numbers in string, it won't split again, and the final position is *N1-q2-4*. By the way, other *NFA*'s states are *q2*, and an *NFA* can receive nothing at *q2*, so they are all "dead" which means the *NFA* doesn't accept this string. However it doesn't matter, because only if there is an *NFA* accepts, then we say the *NFA* accepts the string, and in this example *N1* accepts.

Thus, the string `010` is accepted by this *NFA*.

In a *DFA*, the result of transition function $\delta$ is always a single state $q \in Q$, so its excusing path is always one by one. But due to the nondeterminism, in an *NFA*, the result of its $\delta$ is a state set, so its excusing path can be forked.

Like a *DFA*, we can also define the *NFA* as a 5-tuple, $(Q, \Sigma, \delta, q_0, F)$, and:
1. $Q$ is a finite set called **state set**.
2. $\Sigma$ is a finite set called **alphabet**.
3. $\delta: Q \times \Sigma_\varepsilon \rightarrow P(Q)$ is a **transition function**, and $\Sigma_\varepsilon = \Sigma \cup \varepsilon, P(Q) = \{A\ |\ A \subseteq Q\}$ AKA **power set**.
4. $q_0 \in Q$ is a **start state**.
5. $F \subseteq Q$ is a **set of accept states**.

So, $N_1$ can be defined as $(Q, \Sigma, \delta, q_0, F)$, and:
1. $Q = \{q_1, q_2\}$
2. $\Sigma = \{0, 1\}$
3. $\delta$ can be described as

||0|1|ε|
|---|---|---|---|
|$q_1$|$\{q_2\}$|$\{q_1, q_2\}$|$\{q_2\}$|
|$q_2$|$\varnothing$|$\varnothing$|$\varnothing$|

4. $q_1$ is a **start state**
5. $F = \{q_2\}$

### Connection Between DFA and NFA

> **THEOREM 1**: Given an *NFA*, we can always find a *DFA* which is able to recognize the same language.

Since the result of an *NFA*'s $\delta$ is one of the sets in $P(Q)$, we can treat the set as a state in the target *DFA*.

Assuming an *NFA* 5-tuple is $(Q_1, \Sigma_1, \delta_1, q_1, F_1)$, then we can construct a *DFA* 5-tuple $(Q_2, \Sigma_2, \delta_2, q_2, F_2)$ like this:

1. $Q_2 = P(Q)$
2. $\Sigma_2 = \Sigma_1$
3. If the result of $\delta_1(q,a)$ in *NFA* is *r*($r\subseteq Q$), then we can deduce the result of $\delta_2(\{q\},a)$ is a single state which is equal to *r*. In addition, if 
4. $q_2 = \{q_1\}$
5. $F_2 = \{A\ |\ A \subseteq F\ and\ A \neq \varnothing \}$

By now, we can try to dig out the essence of regular expression.

## Dive Into Regular Expression

### Regular Language

Assuming $M = (Q, \Sigma, \delta, q_0, F)$  is a *DFA*, $w=w_0w_1 \cdots w_n (w_i \in \Sigma)$ is a string. If there is a state sequence $r_0, r_1, \cdots, r_n$, meeting the conditions below:
1. $r_0 = q_0$
2. $\delta (r_i, w_{i+1}) = r_{i+1}, i = 0, 1, \cdots, n-1$
3. $r_n \in F$

Then we say $M$ *accepts* w.

If $A = \{w|M\ accepts\ w\}$, then **M recognizes w**.

> **THEOREM 1**: If a language can be recognized by a *DFA*, it is called **regular language**

### Regular Operation

We define **regular operation**s as below:
1. union: $A \cup B = \{x | x \in A \ or \ x \in B\}$
2. concatenation: $A ○ B = \{xy | x \in A \ and \ y \in B\}$
3. star: $A^* = \{x_1x_2\cdots x_k \ | \ k \geq \ 0 \ and\ x_i \in A \}$

As a mathematic operation's result is also a number, we need to prove a regular operation's result is still a regular language.

#### Union

> **THEOREM 2**: If $A_1$ and $A_2$ are regular languages, then $A_1 \cup A_2$ is a regular language.

[TODO: 链接到DFA那一段]

As we discussed in **DFA**, we know that there is a $M_1$ and a $M_2$ can recognize $A_1$ and $A_2$ separately, since we want to prove that *$A_1 \cup A_2$ is a regular language*, then we need to prove that *there is a $M$ can recognize $A_1 \cup A_2$*.

Let's define $M_1$ as $(Q_1, \Sigma_1, \delta_1, q_1, F_1)$, $M_2$ as $(Q_2, \Sigma_2, \delta_2, q_2, F_2)$ and $M$ as $(Q, \Sigma, \delta, q_0, F)$, then we can figure $M$ out as below:
1. $Q = \{(r_1, r_2)\ |\ r1\in Q_1 \ and \ r_2 \in Q_2\}$
2. $\Sigma = \Sigma_1 \cup \Sigma_2$
3. for $(r_1,r_2) \in Q \ and \ a \in \Sigma$, then $\delta((r_1, r_2), a) = (\delta_1(r_1, a), \delta_2(r_2, a))$
4. $q_0 = (q_1,q_2)$
5. $F = \{(r_1,r_2) \ |\ r_1 \in F_1 \ or \ r_2 \in F_2\}$

For now, we've generated a DFA $M$ recognizing language $A_1 \cup A_2$ which means the result of $A_1 \cup A_2$ is still a **regular language**.

#### Concatenation

> **THEOREM 3**: If $A_1$ and $A_2$ are regular languages, then $A_1 ○ A_2$ is a regular language.

#### Star

> **THEOREM 4**: If $A$ is a regular language, then $A^*$ is a regular language.
