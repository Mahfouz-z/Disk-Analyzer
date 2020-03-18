from treeClasses import *

class parser():
    def __init__(self, disk_tree):
        directoriesDict="tree.txt"
        f=open(directoriesDict, "r")
        self.data=f.read()
        self.parsed=[]
        self.dirc=[]
        self.paths=[]
        self.size=[]
        self.children=[]

        self.parsed = self.data.split("\n") 
        self.total = self.parsed.pop(0) 
        self.parsed.pop(len(self.parsed)-1)
        for i in range(len(self.parsed)):
            if(i%2==1):
                self.children.append(self.parsed[i])
            else:
                self.dirc.append(self.parsed[i])
        for i in range(len(self.dirc)):
            self.dirc[i]= self.dirc[i].split("    ")
        for i in range(len(self.dirc)):
            self.size.append(self.dirc[i][0])
            self.paths.append(self.dirc[i][1])
        self.head = Node(self.paths[0],self.children[0],self.size[0])
        disk_tree.head = self.head
        self.count = 0

    def generate(self, prev): 
        # Save the current number of children to avoid the incrementation of count
        self.num = self.children[self.count]
        if ( int(self.children[self.count]) != 0 ):  # in case fil, appened to the
            for i in range (int(self.num)):
                self.count= self.count +1
                # Create a new node
                current = Node(self.paths[self.count],self.children[self.count],self.size[self.count])
                type=current.npath.split(".")[len(current.npath.split("."))-1]
                if(int(current.nchildrenNump)== 0):
                    current.type=type.split("/")[len(type.split("/"))-1]
                else:
                    current.type= "Folder"
                # if this is a directory, add its children first
                if (int(self.children[self.count]) != 0):
                    self.generate(current)
                # append the new node to the previous
                prev.next.append(current)
