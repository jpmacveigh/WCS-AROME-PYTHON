# coding: utf8
import json
from getWCSCapabilities import getWCSCapabilities
from getWCSCapabilities import mostRecentId
from CoverageId import CoverageId
reso="0025"
code="Kte(h)"
code="Topo"
Id=mostRecentId(reso,code)
if Id:
    Id.describeCoverage()
    print (json.dumps(Id.__dict__,indent=4,sort_keys=True))
    #print Id.coverageId
