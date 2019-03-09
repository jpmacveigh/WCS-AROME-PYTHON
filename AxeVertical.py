#coding: utf8
class AxeVertical:   # un axe vertical défini par les altitudes "valeurs" croissantes de ses points 
    def __init__(self,valeurs):
        self.valeurs=valeurs
    def encadrement(self,z):  # renvoi les deux point de l'axe encadrant l'altitude z
        dernier=len(self.valeurs)-1
        if (len(self.valeurs)<2):
            if (z==self.valeurs[0]): return (self.valeurs[0],self.valeurs[0],0.0)
            else: raise Exception ("AxeVertical : l'axe doit contenir au moins deux points")
        if not(0<=z<=self.valeurs[dernier]) : raise Exception ("AxeVertical : z pas dans l'axe")
        if (z==self.valeurs[0]): return (self.valeurs[0],self.valeurs[1],0.0)
        if (z==self.valeurs[dernier]): return (self.valeurs[dernier-1],self.valeurs[dernier],100.0)
        for i in range(0,len(self.valeurs)):
            if (self.valeurs[i]>=z) :
                zinf=self.valeurs[i-1]
                zsup=self.valeurs[i]
                break
        dist=(z-zinf)/(zsup-zinf)*100.
        return (zinf,zsup,dist)
"""            
import numpy as np
valeurs=np.linspace(0,6325,12,float)
print valeurs
axe=AxeVertical(valeurs)
print axe.encadrement(0)
print axe.encadrement(6325)
print axe.encadrement(1235)
"""