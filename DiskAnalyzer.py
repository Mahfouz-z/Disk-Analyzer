#!/usr/bin/env python3


from treeClasses import *
from parser import *
import subprocess

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import os
import numpy as np

from ui import simpleUi


from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from matplotlib import cm




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
        self.disk_tree = Tree() 
        parserInstance = parser(self.disk_tree)
        parserInstance.generate(self.disk_tree.head)

        self.treeViewPermnanet = QtWidgets.QTreeWidget()
        self.disk_tree.tree_print(self.disk_tree.head, self.treeViewPermnanet)
        print("done parsing the tree!")

    def treeClicked(self, it, col):
        print(it.text(0))

    def analyze(self):
        filePath = self.pathEntry.text()
        if os.path.exists(filePath):
            currentPath = os.getcwd()
            if(filePath[len(filePath)-1] == '/' and len(filePath) != 1):
                filePath = filePath[:-1]
            if(filePath.find(".") != -1):
                filePath.replace(".",currentPath)
            if(filePath == ".."):
                filePath = os.path.normpath(os.getcwd() + os.sep + os.pardir)
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

        x = np.array(sizes)

        self._static_ax = self.static_canvas.figure.subplots()
        self._static_ax.pie(x, shadow=False, startangle=90)
        self._static_ax.legend(labels=labels, loc="upper right", bbox_to_anchor=(1, 1, 0.2, 0.2))

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
    cmd = ["gcc", "-o", "scanner", "scanner.c"] 
    p = subprocess.Popen(cmd)  
    p.wait()  
    os.system('./scanner ' + '/' + ' ' + "> tree.txt")
    print("done producing the tree!")
    app = QtWidgets.QApplication([])
    fb = MyFileBrowser()
    fb.show()
    app.exec_()




