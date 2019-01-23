#coding: utf8
import numpy as np
import math
class Axe:   # un axe avec des ticks et des valeurs définies en ces ticks
    def __init__(self,nom,unit,mini,maxi,nb,valeurs):
        self.nom=nom    # nom de l'axe
        self.unit=unit  # unité
        self.mini=mini  # tick gauche de l'axe (valtick[0])
        self.maxi=maxi  # tick droite de l'axe (vlatick[nb-1]
        self.nb=nb  # nombre de ticks sur l'axe
        if self.nb<2:
            raise Exception("Axe: le nombre de ticks de l'axe %s doit être supérieur ou égal à 2" % self.nb)
        self.valtick=np.linspace(mini,maxi,nb, float)  # liste des nb ticks de l'axe numérotés de 0 à nb-1
        self.valeurs=valeurs # liste des nb valeurs attachées à chaque ticks de l'axe
        if (len(self.valeurs)!=nb):
            raise Exception ("Axe: le nombre de valeurs attachées à l'axe : %s est déférent du nombre de ticks de l' axe : %s" %(len(self.valeurs),self.nb))
    def isInside (self,x):   # test si "x" est dans les limites de l'axe
        return ((self.mini<=x<=self.maxi) or (-self.mini<=-x<=-self.maxi))
    def interval(self,x):  # retourne le premier ticks de l'axes inférieur à la valeur "x"
        if self.isInside(x):
            if x==self.maxi:
                n=self.nb-2
            else:
                n=int((x-self.mini)/(self.maxi-self.mini)*(self.nb-1))
            return (n,(x-self.valtick[n])/(self.valtick[n+1]-self.valtick[n]))
        else:
            raise Exception("Axe.interval(x) : La valeur x=%s n'est pas dans les limites de l'axe qui sont : [ %s , %s ]" %(x, self.mini, self.maxi))
    def val (self,x):  # renvoie la valeur attachée à la position "x" sur l'axe, par interpollation linéaire des valeurs des deux ticks encadrant x
        (ninf,prop)=self.interval(x)
        return (self.valeurs[ninf]+(prop*(self.valeurs[ninf+1]-self.valeurs[ninf])))
            
"""            
nb=2801
#valeurs=np.arange(nb)
valeurs=np.sin(np.arange(nb)/float(nb-1)*math.pi/2.)
axe=Axe("longi","degrés",-12,16.,nb,valeurs)
print axe.valtick
print axe.isInside(5.)
print axe.interval(5.1)
print axe.interval(4.59)
print axe.interval(2.2342)
print axe.interval(0.0)
print axe.interval(10.0)
print axe.interval(9.99)
print axe.val(9.99)
print axe.val(12.4555959)
print axe.val(9.999999999999999)
print axe.val(-12)
print axe.val(2)
print axe.val(16)

"""