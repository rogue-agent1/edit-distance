#!/usr/bin/env python3
"""edit_distance - Multiple edit distance algorithms."""
import argparse

def levenshtein(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            curr[j] = min(curr[j-1]+1, prev[j]+1, prev[j-1]+cost)
        prev = curr
    return prev[n]

def damerau(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s1[i-1]==s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
            if i>1 and j>1 and s1[i-1]==s2[j-2] and s1[i-2]==s2[j-1]:
                dp[i][j] = min(dp[i][j], dp[i-2][j-2]+cost)
    return dp[m][n]

def hamming(s1: str, s2: str) -> int:
    if len(s1) != len(s2): return -1
    return sum(a != b for a, b in zip(s1, s2))

def jaro(s1: str, s2: str) -> float:
    if not s1 and not s2: return 1.0
    if not s1 or not s2: return 0.0
    match_dist = max(len(s1), len(s2)) // 2 - 1
    s1_matches, s2_matches = [False]*len(s1), [False]*len(s2)
    matches = transpositions = 0
    for i in range(len(s1)):
        lo, hi = max(0, i-match_dist), min(i+match_dist+1, len(s2))
        for j in range(lo, hi):
            if s2_matches[j] or s1[i] != s2[j]: continue
            s1_matches[i] = s2_matches[j] = True; matches += 1; break
    if not matches: return 0.0
    k = 0
    for i in range(len(s1)):
        if not s1_matches[i]: continue
        while not s2_matches[k]: k += 1
        if s1[i] != s2[k]: transpositions += 1
        k += 1
    return (matches/len(s1) + matches/len(s2) + (matches-transpositions/2)/matches) / 3

def jaro_winkler(s1: str, s2: str, p: float = 0.1) -> float:
    j = jaro(s1, s2)
    prefix = 0
    for i in range(min(4, len(s1), len(s2))):
        if s1[i] == s2[i]: prefix += 1
        else: break
    return j + prefix * p * (1 - j)

def main():
    p = argparse.ArgumentParser(description="Edit distance calculator")
    p.add_argument("s1"); p.add_argument("s2")
    p.add_argument("-a", "--algorithm", choices=["levenshtein","damerau","hamming","jaro","jaro-winkler","all"], default="all")
    args = p.parse_args()
    algos = {"levenshtein": levenshtein, "damerau": damerau, "hamming": hamming, "jaro": jaro, "jaro-winkler": jaro_winkler}
    if args.algorithm == "all":
        for name, fn in algos.items():
            r = fn(args.s1, args.s2)
            print(f"{name:15s}: {r:.4f}" if isinstance(r, float) else f"{name:15s}: {r}")
    else:
        print(algos[args.algorithm](args.s1, args.s2))

if __name__ == "__main__":
    main()
