from PyQt5 import QtWidgets
# Node class 
class Node: 
   
    # Function to initialize the node object 
    def __init__(self, npath, nchildrenNump,nsize ): 
        self.npath = npath  # Assign path
        self.nchildrenNump = nchildrenNump # Assign Number of Children
        self.nsize = nsize
        self.type = ""
        """type=npath.split(".")[len(npath.split("."))-1]
        if(type==npath):
            self.type="Folder"
        else:
            self.type=type"""
        self.next = []  # Initialize next as list

# Linked List class contains a Node object 
class Tree: 
  
    # Function to initialize head 
    def __init__(self): 
        self.head = None
    def tree_print(self, root, treeView):
        Name = root.npath.split("/")
        Name = Name[len(Name)-1]
        item = QtWidgets.QTreeWidgetItem(treeView, [Name, root.nsize, root.type])
        for child in root.next:
            self.tree_print(child, item)
