def expression2_func(n):
    sum=0
    n=abs(n)
    while(n>0):
        sum+=n%10
        n=n//10
    return sum