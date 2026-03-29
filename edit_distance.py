#!/usr/bin/env python3
"""edit_distance - Levenshtein, Damerau, and weighted edit distance."""
import sys, json

def levenshtein(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s[i-1] == t[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[m][n]

def damerau(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s[i-1] == t[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
            if i > 1 and j > 1 and s[i-1] == t[j-2] and s[i-2] == t[j-1]:
                dp[i][j] = min(dp[i][j], dp[i-2][j-2]+cost)
    return dp[m][n]

def alignment(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s[i-1] == t[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    # Backtrack
    ops = []; i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (0 if s[i-1]==t[j-1] else 1):
            if s[i-1] != t[j-1]: ops.append(f"replace '{s[i-1]}' with '{t[j-1]}'")
            i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j]+1:
            ops.append(f"delete '{s[i-1]}'"); i -= 1
        else:
            ops.append(f"insert '{t[j-1]}'"); j -= 1
    return list(reversed(ops))

def similarity(s, t):
    d = levenshtein(s, t)
    return 1 - d / max(len(s), len(t)) if max(len(s), len(t)) else 1.0

def main():
    print("Edit distance demo\n")
    pairs = [("kitten","sitting"),("saturday","sunday"),("algorithm","altruistic")]
    for s, t in pairs:
        lev = levenshtein(s, t); dam = damerau(s, t); sim = similarity(s, t)
        print(f"  '{s}' -> '{t}': lev={lev}, damerau={dam}, sim={sim:.2f}")
    ops = alignment("kitten", "sitting")
    print(f"\n  Alignment 'kitten'->'sitting': {ops}")

if __name__ == "__main__":
    main()
