#coding: utf8
import datetime
import time
import json
from Vehicule import Vehicule
"""
from getWCSCapabilities import previsions
v=Vehicule (50.635472,3.055083,10.)      # Lille
v.getVentActuelArome()
v.getVentActuelMeteomatics()

tab=previsions ("0025","U(h)",3.055083,50.635472,10)
print (json.dumps(tab,indent=4,sort_keys=True))
tab=previsions ("0025","V(h)",3.055083,50.635472,10)
print (json.dumps(tab,indent=4,sort_keys=True))


v=Vehicule (13.6,103.06,20.)    # Vietnam
v.affiche()
v=Vehicule (50.6,3.06,20.)      # Lille
v.affiche()
v=Vehicule (-22.26,166.15,20.)  # Nouméa
v.affiche()
v=Vehicule (-17.54,-149.57,20.) # Papeete
v.affiche()
"""

#v.getVentActuelMeteomatics()
"""
#reso="0025"
from time import sleep

#v.savePosition()
#v.listPositions()
"""
#v=Vehicule(51.77433177319676,3.862306215709615,200)
#v=Vehicule (-22.26,166.15,20.)  # Nouméa

#v=Vehicule (50.635472,3.055083,20.)      # Lille
#v=Vehicule (48.794954,7.816429,20.)      # Haguenau
#v=Vehicule (44.056286,5.991998,20.)      # Saint-Auban
#v=Vehicule(48.06448117986679,11.180390198888135,10.0)  # Lavey les Bains (Suisse)
#v=Vehicule(44.841662,-0.569312,10)  # Bordeaux
#v=Vehicule(46.5675203751551,4.39642168158707,10);  # Charolles

def initTrajectoire(vehicule):
    print str(datetime.datetime.now())
    print vehicule.ville
    vehicule.savePosition()
    vehicule.listPositions()
def actualiseTrajectoire(vehicule,dt):
    print i,str(datetime.datetime.now())
    vent=vehicule.getVentActuelArome()   # calcul des composante (u,v) actuelles du vent en m/s
    vehicule.moove(vent[0],vent[1],dt)   # on déplace le véhicule à la vitesse du vent
    vehicule=Vehicule(v.lat,v.lng,v.hauteur)  # on recrée un nouveau véhicule à la nouvelle position
    vehicule.savePosition()  # écriture de la nouvelle position dans la trajectoire
    #v.listPositions()
    print (vehicule.ville)
v=Vehicule (42.808021283194975, 9.211713389750136,10)   # la dernière position avant plantage   
initTrajectoire(v)
dt=300. # interval en secondes entre deux actualisations de la trajectoires
for i in range(100000):
    time.sleep(dt)    # wait in seconds
    actualiseTrajectoire(v,dt)
"""
tab=profilVertical (reso,"U(h)",3.06,50.6)
print (json.dumps(tab,indent=4,sort_keys=True))
tab=profilVertical (reso,"V(h)",3.06,50.6)
print (json.dumps(tab,indent=4,sort_keys=True))

print v.dayPhase,v.dayPosition,v.haut,v.lat,v.lng
v.moove(5,5,3600)
print v.dayPhase,v.dayPosition,v.haut,v.lat,v.lng
"""