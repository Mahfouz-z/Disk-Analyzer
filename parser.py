tree={}
def makeTree(paths, children, size, inc, tree):
    r= int(children[inc])
    if(r==0):
        tree[paths[inc]]=size[inc]
        print(str(inc)+"    fil")
        inc+=1
    else:
        for i in range (r):
            tree[paths[inc]]={}
            print(str(inc)+"    fol")
            makeTree(paths, children, size, inc+1, tree[paths[inc]])
            inc+=1





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

well={}
makeTree(paths, children, size, 0, well)
#print(well)
#for i in range (len(paths)):
#    print(well[paths[i]])

