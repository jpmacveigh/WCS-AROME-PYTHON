# coding: utf8
import datetime
import time
import calendar
import requests
import random
from getWCSCapabilities import getWCSCapabilities
from CoverageId import CoverageId
reso="0025"
res=getWCSCapabilities(reso)
print len(res)
res2=[]
for coverageId in res:
    if coverageId.ageRun()<=8 : # on ne traitera que les plus récents
        res2.append(coverageId)
res=res2
print len(res)
i=random.randint(1,len(res))
print res[i].coverageId
print res[i].chaineNom()
print res[i].chaineDate()
print res[i].dateUTCRun()
print res[i].tsUTCRun()
print res[i].ageRun()
print res[i].isCumul()
print res[i].cumul()
print res[i].describeCoverage()
for coverageId in res:
    print " "
    for key in sorted(coverageId.describeCoverage().keys()):
        print ("%s:  %s" % (key,coverageId.describeCoverage()[key]))    