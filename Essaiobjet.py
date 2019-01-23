# coding: utf8
import json
import numpy as np
import time
class toto:
    def __init__(self,x):
        self.longueur=x

print time.time()   
print time.gmtime()
toto=toto(10)
print (json.dumps(toto.__dict__,indent=4))
toto.largeur=23
print (json.dumps(toto.__dict__,indent=4))
cle="hauteur"
toto.__dict__[cle]=56
print (json.dumps(toto.__dict__,indent=4))
cle="altitude"
toto.__dict__[cle]=1450
print (json.dumps(toto.__dict__,indent=4))

tab=np.arange(20).reshape(5,4)
print (tab)
print (tab[0,:])
print(tab[tab.shape[0]-1,:])
print (tab[:,0])
print(tab[:,tab.shape[1]-1])