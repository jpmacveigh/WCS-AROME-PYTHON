# coding: utf8
'''
Classe WCSGeogrib
'''
import pygrib
from Axe import Axe
from Espace2D import Espace2D
import numpy as np
from find_nearest_in_liste import find_nearest_in_liste 
class WCSGeogrib:
    def __init__(self,pathGetCoverage,geogribFileName):
        self.grib=pygrib.open(geogribFileName).message(1)  # on crée un objet pygrib
        self.latitudes=self.grib["distinctLatitudes"]
        self.longitudes=self.grib["distinctLongitudes"]
    
    def description (self):
        print(self.grib)
        print(self.latitudes)
        print(self.longitudes)
        
    def nearest_value (self,longi,lati):
        """
        Renvoi la valeur du champs au point de la grille le plus proche de longi,lati
        """
        i_near,longi_near=find_nearest_in_liste (self.longitudes,longi)
        j_near,lati_near= find_nearest_in_liste (self.latitudes,lati)
        return(
        {"longi_near":longi_near,"lati_near":lati_near,"value":self.grib["values"][j_near][i_near]}
        )
        

"""
        self.dataset = gdal.Open(geogribFileName, gdal.GA_ReadOnly)  # ouverture du fichier geotiff en écriture seule
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
    """
    

"""
filename="WCSgetCoverage.grib"
geogrib=WCSGeogrib("path",filename)
geogrib.description()
print(geogrib.nearest_value(3.06,50.7))
print(geogrib.valeur(3.06,50.7))

print ( geogrib.valeurSurGrille(0,0))   #  coin Ouest-Nord
print ( geogrib.valeurSurGrille(geogrib.RasterXSize-1,geogrib.RasterYSize-1))
print ( geogrib.valeur(geogrib.origineX,geogrib.origineY))
print ( geogrib.valeurInterpolee(geogrib.origineX,geogrib.origineY))
print ( geogrib.valeur(geogrib.extremeX,geogrib.extremeY))
print ( geogrib.valeurInterpolee(geogrib.extremeX,geogrib.extremeY))
print ( geogrib.valeur(3.06,50.6))
print ( geogrib.valeurInterpolee(3.06,50.6))
"""