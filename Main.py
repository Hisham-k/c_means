from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QMessageBox , QSlider , QLabel
import pyqtgraph as pg
from gui import Ui_MainWindow
import os
import sys
import numpy as np
import Project
from PIL import Image

class ApplicationWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', 'w')
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #-----------------------------Constants-----------------------
        self.Cmeans=0

        #----------------Setting up Graphics views--------------------
        self.graphicsViews=[self.ui.graphicsView_1,self.ui.graphicsView_2]

        for i in range(2):
            self.graphicsViews[i].getPlotItem().hideAxis('left')
            self.graphicsViews[i].getPlotItem().hideAxis('bottom')

        #------------button and spinner connections--------------------    
        self.ui.Browse.clicked.connect(self.browse)
        self.ui.spinBox.valueChanged.connect(self.startCluster)

    def browse(self):
            self.filename = QtWidgets.QFileDialog.getOpenFileNames( directory = os.path.dirname(__file__) ,filter= '*.jpeg , *.jpg , *.bmp')
            if((self.filename == ([], '')) | (self.filename ==  0 )):
                return
            print(self.filename[0][0])
            self.extension = os.path.splitext(self.filename[0][0])[1].lower()
            print(self.extension)
            
            try:
                self.graphicsViews[0].removeItem(self.myimage)
            except:
                pass
            
            self.img=Image.open(self.filename[0][0])
            self.myimage=pg.ImageItem(np.asarray(self.img))
            self.myimage.rotate(270)

            self.graphicsViews[0].clear()
            self.graphicsViews[1].clear()
            self.graphicsViews[0].addItem(self.myimage)

    def startCluster(self):
        self.Cmeans=self.ui.spinBox.value()
        if self.Cmeans==(None or 0 or 1):
            return
        result_centroids=Project.main(self.img,self.Cmeans)
        self.drawWindow(result_centroids)

    def drawWindow(self,result_centroids):
        img = Image.new('RGB', (Project.img_width, Project.img_height))
        p = img.load() #RGB pixels of new image
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                RGB_value = result_centroids[Project.getMinDist(Project.px[x, y], result_centroids)] #final assignment of pixel to RGB cluster
                p[x, y] = RGB_value
        #img.show()
        myimage=pg.ImageItem(np.asarray(img))
        myimage.rotate(270)
        self.graphicsViews[1].clear
        self.graphicsViews[1].addItem(myimage)
        #image=ImageOps.grayscale(img)
           




def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()