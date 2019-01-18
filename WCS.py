# coding: utf8
import json
import random
from getWCSCapabilities import mostRecentId
from catalogueWCS import catalogueWCS
reso="0025"
code="Kte(h)"
code="Topo"
#code="Geop(p)"
code="Tmin(h)"
cles=[]
for k,v in catalogueWCS.items():
    cles.append(k)

for i in range(1):
    code=cles[random.randint(0,len(cles)-1)]
    Id=mostRecentId(reso,code)
    if Id:
        Id.describeCoverage()
        print (json.dumps(Id.__dict__,indent=4,sort_keys=True))
        #print Id.coverageId
    if Id.dim==4 :
        Id.getCoverage(48.0,50.0,2.0,3.0,Id.timeDatePrevi[0],Id.niveau(0))
    else:
         Id.getCoverage(48.0,50.0,2.0,3.0,Id.timeDatePrevi[0])