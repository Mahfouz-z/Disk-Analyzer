#!/usr/bin/env python3

from PyQt5.QtCore import QObject
from treeClasses import *
from parser import *


from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import os
import numpy as np

from ui import simpleUi



from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib import cm
import operator
import matplotlib.pyplot as plt


class MyFileBrowser(simpleUi.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, maya=False):
        super(MyFileBrowser, self).__init__()
        self.parseTree()
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pushButton.clicked.connect(self.analyze)
        self.treeView.itemClicked.connect(self.treeClicked)
        self.treeView.setHeaderLabels(["Path", "size", "Type"])
        

    def parseTree(self):
        print("Please Wait, Parsing The Tree...")
        self.disk_tree = Tree() 
        parserInstance = parser(self.disk_tree)
        parserInstance.generate(self.disk_tree.head)
        self.treeViewPermnanet = QtWidgets.QTreeWidget()
        self.disk_tree.tree_print(self.disk_tree.head, self.treeViewPermnanet)
        print("done parsing the tree!")

    def treeClicked(self, it, col):
        if(it.text(2) != "Folder" and it.text(2) != ""):
            it = it.parent()
        path = "/" + it.text(0)
        while(it.parent() != None and it.parent().text(0) != ""):
            path = "/" + it.parent().text(0) + path
            it = it.parent()
        print(path)
        folderHead = Node("","","") 
        self.disk_tree.findHead(self.disk_tree.head, path, folderHead)
        self.setPieChart(folderHead)


    def analyze(self):
        filePath = str(self.pathEntry.text())
        if os.path.exists(filePath):
            currentPath = os.getcwd()
            if(filePath[len(filePath)-1] == '/' and len(filePath) != 1):
                filePath = filePath[:-1]
            if(filePath == "/." or filePath == "/.."):
                filePath = "/"
            if(filePath.find("..") != -1):
                filePath = filePath.replace("..",os.path.normpath(os.getcwd() + os.sep + os.pardir))
            elif(filePath.find(".") != -1):
                filePath = filePath.replace(".",currentPath)
            
            #print(filePath)

            folderHead = Node("","","") 
            self.disk_tree.findHead(self.disk_tree.head, filePath, folderHead)
            #print(folderHead.npath) 
            self.populate(folderHead)
            self.setPieChart(folderHead)
          
        else:
            self.pathEntry.setText("Invalid Path Please Reenter a valid one!")

    def sizeTextToInt(self, size):
        sizeArr = size.split(" ")
        floatSize = float(sizeArr[0])
        sizeArr = sizeArr[::-1]
        if(sizeArr[0] == "GiB"):
            floatSize = floatSize * 10e9
        elif(sizeArr[0] == "MiB"):
            floatSize = floatSize * 10e6
        elif(sizeArr[0] == "KiB"):
            floatSize = floatSize * 10e3
        elif(sizeArr[0] == "TiB"):
            floatSize = floatSize * 10e12  
        return floatSize          
 
    def setPieChart(self, folderHead):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)            
        self.static_canvas = FigureCanvas(Figure(figsize=(10, 6)))
        self.layout.addWidget(self.static_canvas)
        sizes = []
        labels = []
        if(folderHead.nchildrenNump != 0):
            for child in folderHead.next:
                sizes.append(self.sizeTextToInt(child.nsize))
                Name = child.npath.split("/")
                Name = Name[len(Name)-1]
                labels.append(Name)
        else:
            sizes.append(self.sizeTextToInt(child.nsize))
            Name = folderHead.npath.split("/")
            Name = Name[len(Name)-1]
            labels.append(Name)

        #x = np.array(sizes)
        major=[]
        for i in range(len(labels)):
            major.append((labels[i], sizes[i]))
        major=sorted(major, key=operator.itemgetter(1))
        major.reverse()
        s=0.0
        rs=[]
        ls = []
        for i in range(len(major)-9):
            other=major.pop()
            s+=other[1]
        major.append(("others", s))
        for i in range(len(major)):
            rs.append(major[i][1])
            if major[i][0][0]=='_':
                ls.append(' '+major[i][0])
            else:
                ls.append(major[i][0])

        self._static_ax = self.static_canvas.figure.subplots()
        self.theme = plt.get_cmap('jet_r')
        self._static_ax.set_prop_cycle("color", [self.theme(1. * i / len(major))for i in range(len(major))])
        self._static_ax.pie(rs, shadow=False, startangle=90)

        self.total = sum(sizes)
        self._static_ax.legend(labels=['%s, %1.1f%%' % (l, (float(s) / self.total) * 100)for l, s in zip(ls , rs)], loc="upper right", bbox_to_anchor=(1, 1, 0.2, 0.2))
        

    def populate(self, folderHead):
        self.treeView.clear()
        root = self.treeViewPermnanet.invisibleRootItem()
        self.popHelper(folderHead.npath, "", root)
        print("populated")
        self.treeView.setSortingEnabled(True)

    def popHelper(self, path, currentPath, root):
        if(currentPath == path):
            self.treeView.addTopLevelItem(root.clone())
            print("found!")
            path = -1

        child_count = root.childCount()
        for i in range(child_count):
            if(path == -1): return
            item = root.child(i)
            if(currentPath != "/"):
                searchPath =  currentPath + "/" + item.text(0)
            else:
                searchPath =  currentPath + item.text(0)
            if(path.find(searchPath) != -1):
                self.popHelper(path, searchPath, item)
            
                    


if __name__ == '__main__':
    print("Loaing Tree Parser, Please Wait...")
    os.system("gcc -o scanner scanner.c") 
    print("Done Loading Tree Parser!")
    print("Producing The Disk Tree, Please Wait...")
    os.system('./scanner ' + '/' + ' ' + "> tree.txt")
    print("done producing the tree!")
    app = QtWidgets.QApplication([])
    fb = MyFileBrowser()
    fb.show()
    app.exec_()




