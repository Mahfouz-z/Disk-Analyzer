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

# generate random integer values
from random import seed
from random import randint
# seed random number generator
seed(1)


class MyFileBrowser(simpleUi.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, maya=False):
        super(MyFileBrowser, self).__init__()
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pushButton.clicked.connect(self.analyze)
        self.treeView.itemClicked.connect(self.treeClicked)
        self.treeView.setHeaderLabels(["Path", "size", "Type"])


    def treeClicked(self, it, col):
        print(it.text(0))

    def analyze(self):
        filePath = self.pathEntry.text()
        if os.path.exists(filePath):  
            os.system('./scanner ' + filePath + ' ' + "> tree.txt")
            print("done producing the tree!")
            self.disk_tree = Tree() 
            parserInstance = parser(self.disk_tree)
            parserInstance.generate(self.disk_tree.head) 
            print("done parsing the tree!")
            self.populate()
            self.setPieChart(self.disk_tree.head)
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
        cs=cm.Set1(np.arange(40)/40.0)
        self._static_ax.pie(x, shadow=False, startangle=90, colors=cs)
        self._static_ax.legend(labels=labels, loc="upper right", bbox_to_anchor=(1, 1, 0.2, 0.2))

    def populate(self):
        self.treeView.clear()
        self.disk_tree.tree_print(self.disk_tree.head, self.treeView)
        #self.model = QtWidgets.QFileSystemModel()
        #self.model.setRootPath((QtCore.QDir.rootPath()))
        #self.treeView.setModel(self.model)
        #self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)



if __name__ == '__main__':
    cmd = ["gcc", "-o", "scanner", "scanner.c"]; 
    p = subprocess.Popen(cmd);  
    p.wait();   
    app = QtWidgets.QApplication([])
    fb = MyFileBrowser()
    fb.show()
    app.exec_()