# coding: utf8
'''
Classe WCSGeotiff
'''
from Axe import Axe
from Espace2D import Espace2D
import numpy as np
class WCSGeotiff:
    def __init__(self,pathGetCoverage,geotiffFileName):
        import gdal
        self.dataset = gdal.Open(geotiffFileName, gdal.GA_ReadOnly)  # ouverture du fichier geotiff en écriture seule
        #print self.dataset.RasterCount
        if (self.dataset) :
            self.geotransform = self.dataset.GetGeoTransform()
            #print self.geotransform
            self.origineX = self.geotransform[0]
            if (self.origineX > 180.): self.origineX=self.origineX-360.
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
        else :
            print (pathGetCoverage)
            raise Exception ("WCSGeotiff : Fichier geotiff incorrect")
    
    def valeurSurGrille (self,rangLongi,rangLati):  # renvoi la valeur du champ au point de la grille [rangLati,rangLongi]
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
    
    def nearest_value (self,rlongi,rlati):
        """
        Renvoi la valeur du champs au point de la grille le plus proche de rlongi,rlati
        """
        if not(self.origineX <= rlongi <= self.extremeX) : 
            print ("Anomalie rlongi : "+ str(rlongi) + " "+str(self.origineX)+" "+str(self.extremeX))
            raise Exception ("erreur rlongi")
        cmp=lambda x,seuil : -1 if x<seuil else (0 if x==seuil else 1)
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

'''
filename="WCSgetCoverage.tiff"
geotiff=WCSGeotiff(filename)
print geotiff.valeurSurGrille(0,0)   #  coin Ouest-Nord
print geotiff.valeurSurGrille(geotiff.RasterXSize-1,geotiff.RasterYSize-1)
print geotiff.nearest_value(geotiff.origineX,geotiff.origineY)
print geotiff.valeurInterpolee(geotiff.origineX,geotiff.origineY)
print geotiff.nearest_value(geotiff.extremeX,geotiff.extremeY)
print geotiff.valeurInterpolee(geotiff.extremeX,geotiff.extremeY)
print geotiff.nearest_value(3.06,50.6)
print geotiff.valeurInterpolee(3.06,50.6)
'''