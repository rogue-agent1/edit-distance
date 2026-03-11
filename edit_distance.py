#!/usr/bin/env python3
"""Edit distance — Levenshtein, Damerau-Levenshtein, and Hamming distances."""
import sys

def levenshtein(a, b):
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]; dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            dp[j] = min(dp[j]+1, dp[j-1]+1, prev + (0 if a[i-1]==b[j-1] else 1))
            prev = temp
    return dp[n]

def damerau(a, b):
    m, n = len(a), len(b)
    d = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): d[i][0] = i
    for j in range(n+1): d[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1]==b[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
            if i>1 and j>1 and a[i-1]==b[j-2] and a[i-2]==b[j-1]:
                d[i][j] = min(d[i][j], d[i-2][j-2]+cost)
    return d[m][n]

def hamming(a, b):
    if len(a) != len(b): return -1
    return sum(x != y for x, y in zip(a, b))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        pairs = [("kitten","sitting"),("saturday","sunday"),("hello","hallo")]
        for a, b in pairs:
            print(f"  {a!r} → {b!r}: lev={levenshtein(a,b)} dam={damerau(a,b)}")
    else:
        a, b = sys.argv[1], sys.argv[2]
        print(f"Levenshtein: {levenshtein(a, b)}")
        print(f"Damerau-Lev: {damerau(a, b)}")
        if len(a) == len(b): print(f"Hamming:     {hamming(a, b)}")
