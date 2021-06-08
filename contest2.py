t=int(input())
for _ in range(t):
    n=int(input())
    li=[int(x) for x in input().split(" ")]
    min=abs(sum(li[:1])-sum(li[1:]))
    for i in range(len(li)-2):
        if min>abs(sum(li[:2+i])-sum(li[2+i:])):
            min=abs(sum(li[:2+i])-sum(li[2+i:]))
    print(min)