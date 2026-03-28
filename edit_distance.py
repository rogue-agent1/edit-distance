#!/usr/bin/env python3
"""Edit distance (Levenshtein) with alignment."""
import sys
def edit_distance(a,b):
    m,n=len(a),len(b)
    dp=[[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0]=i
    for j in range(n+1): dp[0][j]=j
    for i in range(1,m+1):
        for j in range(1,n+1):
            if a[i-1]==b[j-1]: dp[i][j]=dp[i-1][j-1]
            else: dp[i][j]=1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])
    # Backtrace
    ops=[];i,j=m,n
    while i>0 or j>0:
        if i>0 and j>0 and a[i-1]==b[j-1]: ops.append(('match',a[i-1]));i-=1;j-=1
        elif i>0 and j>0 and dp[i][j]==dp[i-1][j-1]+1: ops.append(('replace',a[i-1],b[j-1]));i-=1;j-=1
        elif i>0 and dp[i][j]==dp[i-1][j]+1: ops.append(('delete',a[i-1]));i-=1
        else: ops.append(('insert',b[j-1]));j-=1
    return dp[m][n],list(reversed(ops))
def main():
    if "--demo" in sys.argv:
        pairs=[("kitten","sitting"),("saturday","sunday"),("algorithm","altruistic")]
        for a,b in pairs:
            d,ops=edit_distance(a,b)
            edits=[o for o in ops if o[0]!='match']
            print(f"'{a}' → '{b}': distance={d}, ops={edits}")
    elif len(sys.argv)>2:
        d,_=edit_distance(sys.argv[1],sys.argv[2]);print(d)
if __name__=="__main__": main()
