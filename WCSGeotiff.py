# coding: utf8
import gdal
from Axe import Axe
from Espace2D import Espace2D
import numpy as np
class WCSGeotiff:
    def __init__(self,geotiffFileName):
        self.dataset = gdal.Open(geotiffFileName, gdal.GA_ReadOnly)  # ouvertif du fichier geotiff en écriture seule
        #print self.dataset.RasterCount
        self.geotransform = self.dataset.GetGeoTransform()
        #print self.geotransform
        self.origineX = self.geotransform[0]
        self.origineY = self.geotransform[3]
        self.pixelWidth = self.geotransform[1]
        self.pixelHeight = self.geotransform[5]
        self.RasterXSize=self.dataset.RasterXSize
        self.extremeX=self.origineX+self.RasterXSize*self.pixelWidth
        self.RasterYSize=self.dataset.RasterYSize
        self.extremeY=self.origineY+self.RasterYSize*self.pixelHeight
        #print("Origin = ({}, {})".format(self.origineX,self.origineY))
        #print("Extrem = ({}, {})".format(self.extremeX,self.extremeY))
        #print("Pixel Size = ({}, {})".format(self.pixelWidth,self.pixelHeight))
        #print("Raster Size = (X={}, Y={})".format(self.RasterXSize, self.RasterYSize))
        self.band = self.dataset.GetRasterBand(1)
        self.array=self.band.ReadAsArray()
        self.valMin=self.array.argmin()
        self.valMax=self.array.argmax()
        self.valMoy=self.array.mean()
        self.axeLongi=Axe("longi","deg",self.geotransform[0],self.geotransform[0]+(self.RasterXSize)*self.geotransform[1],self.RasterXSize,np.arange(self.RasterXSize))
        self.axeLati =Axe("lati", "deg",self.geotransform[3],self.geotransform[3]+(self.RasterYSize)*self.geotransform[5],self.RasterYSize,np.arange(self.RasterYSize))
        self.espace2D=Espace2D(self.axeLongi,self.axeLati,self.array)
        #print type(self.array)
        #print self.array.shape
    def valeurSurGrille(self,rangLongi,rangLati):  # renvoi la valeur du champ au point de la grille [rangLati,rangLongi]
        if not (0<= rangLongi <= self.dataset.RasterXSize-1): raise Exception ("erreur rangLongi")
        if not (0<= rangLati <= self.dataset.RasterYSize-1): raise Exception ("erreur rangLati")
        rlongi = self.geotransform[0] + rangLongi*self.geotransform[1] + rangLati*self.geotransform[2]
        rlati = self.geotransform[3] + rangLongi*self.geotransform[4] + rangLati*self.geotransform[5]
        val=self.array[rangLati,rangLongi]
        return rlongi,rlati,val
    def valeurInterpolee (self,rlongi,rlati):  # renvoi la valeur du champs interpolée sur la grille
        # comme moyene des valeurs des 4 points entourants la position (longi,lati)
        # pondérée par l'inverse de la distance orthodromique à chacun des 4 points 
        return self.espace2D.valeur(rlongi,rlati)
    def valeur (self,rlongi,rlati):
        if not(self.origineX <= rlongi <= self.extremeX) : raise Exception ("erreur rlongi")
        s=cmp(self.pixelHeight,0)
        if not(self.origineY*s <= s*rlati <= s*self.extremeY) : raise Exception ("erreur rlati")
        if rlongi==self.extremeX:
            xOffset=self.RasterXSize-1
        else:
            xOffset = int((rlongi-self.origineX)/self.pixelWidth)
        if rlati==self.extremeY:
            yOffset=self.RasterYSize-1
        else:
            yOffset = int((rlati -self.origineY)/self.pixelHeight)
        #print (xOffset,yOffset)
        return (self.array[yOffset,xOffset])
"""
filename="WCSgetCoverage.tiff"
geotiff=WCSGeotiff(filename)
print geotiff.valeurSurGrille(0,0)   #  coin Ouest-Nord
print geotiff.valeurSurGrille(geotiff.RasterXSize-1,geotiff.RasterYSize-1)
print geotiff.valeur(geotiff.origineX,geotiff.origineY)
print geotiff.valeurInterpolee(geotiff.origineX,geotiff.origineY)
print geotiff.valeur(geotiff.extremeX,geotiff.extremeY)
print geotiff.valeurInterpolee(geotiff.extremeX,geotiff.extremeY)
print geotiff.valeur(3.06,50.6)
print geotiff.valeurInterpolee(3.06,50.6)
"""