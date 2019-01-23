# coding: utf8
import gdal
filename="WCSgetCoverage.tiff"
ds = gdal.Open(filename, gdal.GA_ReadOnly)  # ouvertif du fichier geotiff en écriture seule
print ds.RasterXSize
print ds.RasterYSize
print ds.RasterCount
geotransform = ds.GetGeoTransform()
print geotransform
originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]
print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
GT=geotransform
geotransform = ds.GetGeoTransform()
band = ds.GetRasterBand(1)
array=band.ReadAsArray()
def geo(rangLongi,rangLati):
    if not (0<= rangLongi <= ds.RasterXSize-1): raise Exception ("erreur rangLongi")
    if not (0<= rangLati <= ds.RasterYSize-1): raise Exception ("erreur rangLati")
    longi = GT[0] + rangLongi*GT[1] + rangLati*GT[2]
    lati = GT[3] + rangLongi*GT[4] + rangLati*GT[5]
    val=array[rangLati,rangLongi]
    return longi,lati,val
print geo(560,480)
print geo(0,0)
band = ds.GetRasterBand(1)
array=band.ReadAsArray()
print type(array)
print array.shape