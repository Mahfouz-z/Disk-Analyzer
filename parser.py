directoriesDict="tree.txt"
f=open(directoriesDict, "r")
data=f.read()
parsed=[]
dirc=[]
paths=[]
size=[]
children=[]
parsed = data.split("\n") 
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



# Node class 
class Node: 
   
    # Function to initialize the node object 
    def __init__(self, npath, nchildrenNump,nsize ): 
        self.npath = npath  # Assign path
        self.nchildrenNump = nchildrenNump # Assign Number of Children
        self.nsize = nsize
        type=npath.split(".")[len(npath.split("."))-1]
        if(type==npath):
            self.type="Folder"
        else:
            self.type=type
        self.next = []  # Initialize next as list

# Linked List class contains a Node object 
class Tree: 
  
    # Function to initialize head 
    def __init__(self): 
        self.head = None
    def tree_print(self,root):
        print(root.npath,"\t",root.nsize, root.type)
        for child in root.next:
            self.tree_print(child)


#test="test.txt"
#w=open(test, "a")


disk_tree = Tree() 
head = Node(paths[0],children[0],size[0])
disk_tree.head = head

count = 0

def generate(prev): 
    global count
    # Save the current number of children to avoid the incrementation of count
    num = children[count]
    if ( int(children[count]) != 0 ):  # in case fil, appened to the
        for i in range (int(num)):
            count= count +1
            # Create a new node
            current = Node(paths[count],children[count],size[count])
            # if this is a directory, add its children first
            if (int(children[count]) != 0):
                generate(current)
            # append the new node to the previous
            prev.next.append(current)


# head is now the root of the tree
generate(disk_tree.head)
disk_tree.tree_print(disk_tree.head)

print("DONE")
