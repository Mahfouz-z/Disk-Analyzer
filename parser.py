directoriesDict="tree.txt"
f=open(directoriesDict, "r")
data=f.read()
parsed=[]
dirc=[]
paths=[]
size=[]
children=[]
parsed=data.split("\n")
total= parsed.pop(0)
parsed.pop(len(parsed)-1)
for i in range(len(parsed)):
    if(i%2==1):
        children.append(parsed[i])
    else:
        dirc.append(parsed[i])
for i in range(len(dirc)):
    dirc[i]= dirc[i].split("    ")
for i in range(len(dirc)):
    size.append(dirc[i][0])
    paths.append(dirc[i][1])


print(parsed)


def makeTree(paths, children, size):
    tree={}
