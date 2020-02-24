#! /usr/bin/python
# -*- coding:utf-8 -*-
from VentHorizontal import VentHorizontal
import math
class VentHorizontal_DDFF:
  def __init__ (self,dd,ff):
    self.dd=dd
    self.ff=ff
    self.u=-math.sin(math.radians(dd))*ff
    self.v=-math.cos(math.radians(dd))*ff
    self.vent_UV=VentHorizontal(self.u,self.v)
    assert abs(dd - self.vent_UV.direction())  <= 10.**-6, (dd, self.vent_UV.direction())
    assert abs(ff - self.vent_UV.vitesse_ms()) <= 10.**-6, (ff,self.vent_UV.vitesse_ms())
  def vitesse_kmh(self): 
        return (self.ff*3.6);
  def vitesse_kt(self):
        return (self.ff*3600./1852.);
  def direction360(self):
        return int(round(self.dd));
  def direction36(self):
        return int(round(self.dd/10.));
  def toStringKmh(self):
        x=str(self.direction360()).zfill(3)
        return (x+"/"+str(int(round(self.vitesse_kmh(),0)))+" km/h")
  def affiche(self):
        for k in self.__dict__:
            print (k,self.__dict__[k])
'''  

v=VentHorizontal_DDFF(185.534,1.821)
print (v.dd,v.ff,v.u,v.v,v.vent_UV.toStringKmh(),v.vent_UV.vitesse_kmh())

v=VentHorizontal_DDFF(0.,1.821)
print (v.dd,v.ff,v.u,v.v,v.vent_UV.toStringKmh(),v.vent_UV.vitesse_kmh())

v=VentHorizontal_DDFF(45.,1.821)
print (v.dd,v.ff,v.u,v.v,v.vent_UV.toStringKmh(),v.vent_UV.vitesse_kmh())

v=VentHorizontal_DDFF(135.,1.821)
print (v.dd,v.ff,v.u,v.v,v.vent_UV.toStringKmh(),v.vent_UV.vitesse_kmh())

v=VentHorizontal_DDFF(225.,1.821)
print (v.dd,v.ff,v.u,v.v,v.vent_UV.toStringKmh(),v.vent_UV.vitesse_kmh())

v=VentHorizontal_DDFF(315.,1.821)
print (v.dd,v.ff,v.u,v.v,v.vent_UV.toStringKmh(),v.vent_UV.vitesse_kmh())

v=VentHorizontal_DDFF(360.,1.821)
print (v.dd,v.ff,v.u,v.v,v.vent_UV.toStringKmh(),v.vent_UV.vitesse_kmh())

'''