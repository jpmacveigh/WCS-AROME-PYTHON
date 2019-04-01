#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
class VentHorizontal :  # Un vent horizontal défini par sa composante zonale u (Ouest-Est, positive vers l'Est) et méridienne v (Sud-Nord, positive vers le Nord) en m/s
    def __init__(self,u,v):
        self.u=u
        self.v=v
    def vitesse_ms(self):
        return (math.sqrt (self.u*self.u + self.v*self.v));
    def vitesse_kmh(self): 
        return (self.vitesse_ms()*3.6);
    def vitesse_kt(self):
        return (self.vitesse_ms()*3600./1852.);
    def direction(self):  # direction du vent, par convention, celle d'où il vient.
        if ((self.u==0.)and(self.v==0.)):  return 0.
        else: return ((math.atan2(self.u,self.v)/math.pi +1)*180.)  # calcul faux en zone polaire. A revoir
    def direction360(self):
        return int(round(self.direction()));
    def direction36(self):
        return int(round(self.direction()/10.));
    def capVitesse(self):  # renvoit le cap suivi et la vitesse d'une particule qui se déplacerait avec ce vent horizontal
       cap = self.direction()+180.
       if (cap>360.): cap=cap-360.
       return (cap,self.vitesse_ms())
    def toStringKmh(self):
        x=str(self.direction360()).zfill(3)
        return (x+"/"+str(int(round(self.vitesse_kmh(),0)))+" km/h")
        


v=VentHorizontal(-3,-3)
print v.direction()
print v.direction360()
print v.direction36()
print v.vitesse_kmh()
print v.vitesse_ms()
print v.vitesse_kt()
print v.capVitesse()
print v.toStringKmh()

