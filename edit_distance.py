#!/usr/bin/env python3
"""Edit distance algorithms — Levenshtein, Damerau, Hamming, Jaro-Winkler."""
import sys

def levenshtein(a, b):
    m, n = len(a), len(b)
    dp = list(range(n+1))
    for i in range(1, m+1):
        prev, dp[0] = dp[0], i
        for j in range(1, n+1):
            temp = dp[j]
            dp[j] = min(dp[j]+1, dp[j-1]+1, prev + (a[i-1] != b[j-1]))
            prev = temp
    return dp[n]

def damerau(a, b):
    m, n = len(a), len(b)
    d = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): d[i][0] = i
    for j in range(n+1): d[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
            if i > 1 and j > 1 and a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                d[i][j] = min(d[i][j], d[i-2][j-2]+cost)
    return d[m][n]

def hamming(a, b):
    if len(a) != len(b): raise ValueError("Strings must be equal length")
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def jaro(a, b):
    if not a and not b: return 1.0
    if not a or not b: return 0.0
    window = max(len(a), len(b)) // 2 - 1
    a_matches = [False]*len(a)
    b_matches = [False]*len(b)
    matches = transpositions = 0
    for i in range(len(a)):
        lo, hi = max(0, i-window), min(len(b), i+window+1)
        for j in range(lo, hi):
            if b_matches[j] or a[i] != b[j]: continue
            a_matches[i] = b_matches[j] = True
            matches += 1
            break
    if not matches: return 0.0
    k = 0
    for i in range(len(a)):
        if not a_matches[i]: continue
        while not b_matches[k]: k += 1
        if a[i] != b[k]: transpositions += 1
        k += 1
    return (matches/len(a) + matches/len(b) + (matches-transpositions/2)/matches) / 3

def test():
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("", "abc") == 3
    assert damerau("ca", "ac") == 1  # transposition
    assert hamming("karolin", "kathrin") == 3
    j = jaro("martha", "marhta")
    assert abs(j - 0.9444) < 0.01
    print("  edit_distance: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Edit distance algorithms")
