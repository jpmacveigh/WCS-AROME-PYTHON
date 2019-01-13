# coding: utf8
import json
class toto:
    def __init__(self,x):
        self.longueur=x

    
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