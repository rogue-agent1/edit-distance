#!/usr/bin/env python3
"""edit_distance - Levenshtein and other string distances."""
import sys

def levenshtein(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

def damerau(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
            if i > 1 and j > 1 and a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                dp[i][j] = min(dp[i][j], dp[i-2][j-2]+cost)
    return dp[m][n]

def hamming(a, b):
    if len(a) != len(b): raise ValueError("Equal length required")
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def similarity(a, b):
    d = levenshtein(a, b); mx = max(len(a), len(b))
    return 1 - d/mx if mx else 1.0

if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: edit_distance.py <str1> <str2> [--type lev|dam|ham]"); sys.exit(1)
    a, b = sys.argv[1], sys.argv[2]
    t = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--type" else "lev"
    fns = {"lev": levenshtein, "dam": damerau, "ham": hamming}
    d = fns[t](a, b)
    print(f"Distance ({t}): {d}"); print(f"Similarity: {similarity(a,b):.2%}")
