# coding: utf8
import json
import random
from getWCSCapabilities import mostRecentId
from getWCSCapabilities import profilVertical
from CatalogueWCS import CatalogueWCS
reso="0025"
#code="Kte(h)"
#code="Topo"
#code="Geop(p)"
#code="Tmin(h)"
"""

cles=[]
for k,v in catalogueWCS.items():
    cles.append(k)

for i in range(20):
    code=cles[random.randint(0,len(cles)-1)]
   
    code="Kte(h)"
    code="Tmin(h)"
    code="Tmax(h)"
   
    Id=mostRecentId(reso,code)
    if Id:
        Id.describeCoverage()
        if Id.dim==4 : # getCoverage sur un domaine couvrant la France
            Id.getCoverage(41.0,53.0,-6.0,8.0,Id.timeDatePrevi[0],Id.niveau(0))
        else:
             Id.getCoverage(41.0,53.0,-6.0,8.0,Id.timeDatePrevi[0])
        #print (json.dumps(Id.__dict__,indent=4,sort_keys=True))
        
        #print Id.valeur(0,0)
        def imprime (obj):  # imprime tous les attributs d'un objet dans l'ordre alphabétique de ses clés
            for cle in sorted(obj.__dict__): print ("%s: %s" %(cle,obj.__dict__[cle]))
        #imprime (Id)
       
        print Id.axeLongi.nb
        print Id.axeLongi.valtick
        print Id.axeLati.nb
        print Id.axeLati.valtick
        print Id.code,Id.nivGot,Id.unite,Id.chaineDatePreviGot,Id.espace2D.valeur(3.06,50.6)
        #print (json.dumps(Id.__dict__,indent=4,sort_keys=True))
 """      

for code in CatalogueWCS().cles() :
    #code="T(h)"
    #print code
    tab=profilVertical (reso,code,3.06,50.6)
    #print tab
    print (json.dumps(tab,indent=4,sort_keys=True))
"""
code="Tmin(h)"
#print code
tab=profilVertical (reso,code,3.06,50.6)
print (json.dumps(tab,indent=4,sort_keys=True))
"""