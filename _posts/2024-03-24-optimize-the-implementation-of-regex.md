---
layout: post
title: "Optimize the Implementation of Regex"
date: 2024-03-24 16:10:58 +0800
published: true
categories: [Implementation, Finite Automaton]
tags: [finite automaton, regular expression]
# The categories of each post are designed to contain up to two elements, and the number of elements in tags can be zero to infinity. 
# TAG names should always be lowercase
author: max
toc: true
comments: false
math: true
mermaid: true
# Mermaid is a great diagram generation tool
---

> Before reading this article, you might want to read [Implement A Tiny Regular Expression](/posts/implement-a-tiny-regular-expression/) first for understanding more easily.
{: .prompt-tip }

## Simplify the *NFA*

It's not easy to simplify an *NFA* directly, but to simplify a *DFA* is relatively easily. 
So, we can convert the *NFA* to *DFA*, then simplify the *DFA*, and finally, we can get a streamlined *NFA* by converting it back.

## Define *DFA*

*DFA* is mostly like an *NFA*, except it doesn't have ε and its δ's result is a single state instead of a set of state.

```c++
class DFA
{
    int Q; // Due to all the states are numbers, we can use the count of states to represent all possible states, and the range is 0-(Q-1).
    set<char> Σ;
    vector<map<char, int>> δ;
    int q; // The start state.
    set<int> F;    
}
```

## Convert *NFA* to *DFA*

According to what we discussed in [A Deeper Understanding of Regular Expression](/posts/a-deeper-understanding-of-regular-expression/#relationship-between-dfa-and-nfa), the key moving is to convert P(Q) into a single state. So let's add a constructor to *DFA*.

```c++
DFA::DFA(const NFA& n)
{
    Σ = n.Σ; // Σ are just the same.
    vector<map<char, set<int>>> tempDelta; // Used to get DFA's δ
    map<set<int>, int> N2DConverter; // A map stores the relationship between NFA's states set and DFA's state.
    int stateIndex = 0; // Used to indicate current DFA's state
    queue<set<int>>> stateSetQueue = {n.calculateEpsilonReachableStates({n.q})}; // Let's start from n.q

    while (!stateSetQueue.empty()) {
        set<int> states = stateSetQueue.front();
        stateSetQueue.pop();
        map<int, set<int>> tempmap;

        for (int c: Σ) {
            set<int> resStates;
            for (int s: states) {
                if (δ[s].contains(c)) {
                    resStates.insert(δ[s][c].begin(), δ[s][c].end());
                }
            }
            resStates = n.calculateEpsilonReachableStates(resStates);
            tempmap[c] = resStates;
            if (!N2dConverter.contains(resStates)) {
                stateSetQueue.push(resStates);
            }
        }
        tempDelta.emplace(tempmap);
        N2dConverter[states] = stateIndex;
        stateIndex++;
    }

    for (int i = 0; i < stateIndex; i++) {
        δ.emplace_back({});
        for (auto m: tempDelta[i]) {
            δ[i][m.first] = N2dConverter[m.second];
        }
    }
}
```

## Reduce the Count of *DFA*'s States

1. Divide all states into 2 groups, one consists of all accept states, the other contains other states;
2. Choose a symbol from Σ, calculate the result state with the state from the same group;
3. If a state's result state is from a different group, then put this state to a new group, if another state's result state is from the same group as this one, put it into the new group;
4. Repeat step 2-3 until there's no new group;
5. Update states.

```c++
void DFA::simplify(void)
{
    vector<StateGroupInfo> groups = vector<StateGroupInfo>(Q, StateGroupInfo{0, 0});
    int acceptStatesGroupNum = F.size() == Q ? 0 : 1;
    for (int s = 0; s < Q; s++) {
        if (isAcceptState(s)) {
            groups[s].groupNum = acceptStatesGroupNum;
        }
    }

    map<StateGroupInfo, int> newStateGroupMap;
    int resState;
    int currentStateCount = acceptStatesGroupNum + 1;
    int symbol;

    int i = Σ.begin();
    while (i != Σ.end()) {

        newStateGroupMap.clear();

        for (int j = 0; j < Q; j++) {

            resState = δ[j][symbol];
            groups[j].resultGroupNum = groups[resState].groupNum;
            if (newStateGroupMap.find(groups[j]) == newStateGroupMap.end()) {
                newStateGroupMap[groups[j]] = (int)newStateGroupMap.size();
            }
        }

        if (newStateGroupMap.size() > currentStateCount) {

            for (int j = 0; j < Q; j++) {
                groups[j].groupNum = newStateGroupMap[groups[j]];
            }
            currentStateCount = (int)newStateGroupMap.size();

            i = Σ.begin() - 1;
        }
        i++;
    }

    map<int, map<int, int>> tempTransition;
    set<int> tempAcceptStates;

    for (int i = 0; i < Q; i++) {

        if (isAcceptState(i)) {
            tempAcceptStates.insert(groups[i].groupNum);
        }
        for (int symbol: Σ) {
            tempTransition[groups[i].groupNum][symbol] = groups[δ[i][symbol]].groupNum;
        }
    }

    Q = currentStateCount;
    q = groups[q].groupNum;
    F = tempAcceptStates;

    δ.clear();
    for (int i = 0; i < currentStateCount; i++) {
        δ.emplace_back(tempTransition[i]);
    }
}
```

## Convert *DFA* to *NFA*

Before converting, let me introduce a state called **terminal state**. for any s in Q and any c in Σ, δ[s][c] = s, then we say the s is a **terminal state**.

Because the result of a *DFA*'s δ is a single state, so we just need to transfer the single state into a set.

But pay attention to the **terminal state** in *DFA*, it should be treated as an empty set in *NFA*, which means it should be deleted.

```c++
NFA::NFA(const DFA& d)
{
    Q = d.Q - (int)d.terminalStates.size();
    Σ = d.Σ;
    F = {};
    δ = {};

    vector<int> newStatesMap(d.Q);
    vector<int> dterminal{d.terminalStates.begin(), d.terminalStates.end()};
    std::sort(dterminal.begin(), dterminal.end());

    for (int i = 0; i < d.Q; i++) {
        newStatesMap[i] = i - (int)(std::lower_bound(dterminal.begin(), dterminal.end(), i) - dterminal.begin());
    }

    map<int, set<int>> tempMap = {};

    for (int i = 0; i < d.Q; i++) {
        if (!d.isTerminalState(i)) {
            for (auto it = d.δ[i].begin(); it != d.δ[i].end(); it++) {
                if (!d.isTerminalState(it->second)) {
                    tempMap[it->first] = {newStatesMap[it->second]};
                }
            }
            δ.emplace_back(tempMap);
            tempMap.clear();
        }
    }

    q = newStatesMap[d.q];
    for (auto s: d.F) {
        F.insert(newStatesMap[s]);
    }
}
```

For now, we have finished simplifying an *NFA*.
You can get all codes [here](https://github.com/ssase/regex).
