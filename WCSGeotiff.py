# coding: utf8
import gdal
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
        #print type(self.array)
        #print self.array.shape
    def valeurSurGrille(self,rangLongi,rangLati):
        if not (0<= rangLongi <= self.dataset.RasterXSize-1): raise Exception ("erreur rangLongi")
        if not (0<= rangLati <= self.dataset.RasterYSize-1): raise Exception ("erreur rangLati")
        longi = self.geotransform[0] + rangLongi*self.geotransform[1] + rangLati*self.geotransform[2]
        lati = self.geotransform[3] + rangLongi*self.geotransform[4] + rangLati*self.geotransform[5]
        val=self.array[rangLati,rangLongi]
        return longi,lati,val
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
print geotiff.valeur(geotiff.extremeX,geotiff.extremeY)
print geotiff.valeur(3.06,50.6)
"""
