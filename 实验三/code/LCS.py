def merge(x, y, lcslist, i, j, output, outputlist):
    temp = lcslist[i][j]
    flag = False
    if temp == 0:
        output = output[::-1]
        if output not in outputlist:
            outputlist.append(output)
        return

    if lcslist[i][j-1] == temp:
        merge(x,y,lcslist,i,j-1,output,outputlist)
        flag = True
    if lcslist[i-1][j] == temp:
        merge(x,y,lcslist,i-1,j,output,outputlist)
        flag = True

    if flag == False:
        output += x[i-1]
        merge(x,y,lcslist,i-1,j-1,output,outputlist)

x = input("x:")
y = input("y:")
m = len(x)
n = len(y)
lcslist = [[0 for i in range(n + 1)] for j in range(m + 1)]
for i in range(m):
    for j in range(n):
        if x[i] == y[j]:
            lcslist[i+1][j+1] = lcslist[i][j] + 1
        elif lcslist[i+1][j] >= lcslist[i][j+1]:
            lcslist[i+1][j+1] = lcslist[i+1][j]
        else:
            lcslist[i+1][j+1] = lcslist[i][j+1]

print(lcslist)
output=""
outputlist=[]
merge(x, y, lcslist, m, n, output, outputlist)
print(outputlist)