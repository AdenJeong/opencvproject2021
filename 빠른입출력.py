import sys

N = int(sys.stdin.readline())
for i in range(N):
    inp = sys.stdin.readline()
    print("%d. %s" %(i+1, inp), end="")