n = int(input())
sp = [map(int, input().split())]

for i in range(int(input())):
    s = list(map(str, input().split()))
    if s[0] == 'u':
        sp[int(s[1])] = int(s[2])
    else:
        sp[int(s[1])] = int(s[2])
