res=""
a="-"
n=4
cur=100
c='f'
res+="+"*n+"[<"+a*n+">-]<"+a*(abs(cur-ord(c))-n*n)+".>"
print(res)