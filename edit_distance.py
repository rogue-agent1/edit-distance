#!/usr/bin/env python3
"""Edit Distance — Levenshtein, Damerau-Levenshtein, alignment."""
import sys

def levenshtein(s, t):
    m, n = len(s), len(t)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            temp = dp[j]
            dp[j] = min(dp[j] + 1, dp[j-1] + 1, prev + (0 if s[i-1] == t[j-1] else 1))
            prev = temp
    return dp[n]

def damerau_levenshtein(s, t):
    m, n = len(s), len(t)
    d = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): d[i][0] = i
    for j in range(n+1): d[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s[i-1] == t[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
            if i > 1 and j > 1 and s[i-1] == t[j-2] and s[i-2] == t[j-1]:
                d[i][j] = min(d[i][j], d[i-2][j-2]+cost)
    return d[m][n]

def alignment(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+(0 if s[i-1]==t[j-1] else 1))
    # Traceback
    a1, a2 = [], []; i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (0 if s[i-1]==t[j-1] else 1):
            a1.append(s[i-1]); a2.append(t[j-1]); i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            a1.append(s[i-1]); a2.append('-'); i -= 1
        else:
            a1.append('-'); a2.append(t[j-1]); j -= 1
    return ''.join(reversed(a1)), ''.join(reversed(a2))

if __name__ == "__main__":
    pairs = [("kitten","sitting"), ("saturday","sunday"), ("abc","ca")]
    for s, t in pairs:
        print(f"  {s} → {t}: lev={levenshtein(s,t)}, damerau={damerau_levenshtein(s,t)}")
    a1, a2 = alignment("INTENTION", "EXECUTION")
    print(f"\nAlignment:\n  {a1}\n  {a2}")
