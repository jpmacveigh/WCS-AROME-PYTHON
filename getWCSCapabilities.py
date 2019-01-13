# coding: utf8
from __future__ import unicode_literals
import requests
import sys
from CoverageId import CoverageId
#import xml.etree.ElementTree as ET
from xml.dom import minidom
def getWCSCapabilities(resol):  # Lance une requête "getCapabilities" du WCS pour le modèel Arome de MF. La résolution ("0025" ou "001") est donnée en paramètre. 
    path="https://geoservices.meteofrance.fr/services/MF-NWP-HIGHRES-AROME-"
    path=path+resol+"-FRANCE-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"
    #curl "https://geoservices.meteofrance.fr/services/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__" > resultGetCapabilities
    status=-1
    while status != 200:
        r=requests.get(path)
        status=r.status_code
    fichier = open("WCSCapabilities.xml","w")
    print >> fichier,r.content  # le résultat de la requête est un XML qui l'on écrite dans un ficheir
    fichier.close()
    mydoc = minidom.parse("WCSCapabilities.xml")  # parse an XML file given by his name
    items = mydoc.getElementsByTagName('wcs:CoverageId') # recherches des CoverageID dans le ficheir XML parsé
    res=[];
    lesTitres=set()
    cle={}
    for i in range (0,len(items)):  # boucle sur les CoverageId trouvés dans le fichier XML parsé
        coverageId=items[i].childNodes[0].nodeValue  # le coverageId
        node=items[i].parentNode
        node=node.getElementsByTagName('ows:Title')  # recherche de sa description
        description=node[0].childNodes[0].nodeValue  # sa description
        cle='"",("'+CoverageId(coverageId,resol).chaineNom()+'","'+description+'"),'
        lesTitres.add(cle)
        cov=CoverageId(coverageId,resol)  # création dun objet CoverageId
        cov.descr=description  # renseignement de sa descritpion
        res.append(cov)  # écriture des objets CoverageId dans la liste des résultats
    titres=sorted(lesTitres)
    """for titre in titres:
        print titre
    print len(titres)"""
    
    return res    # renvoi la liste des objets CoverageId exposés par le WCS de MF
def mostRecentId(resol,code):
    tab=getWCSCapabilities(resol)
    ts=-sys.maxint-1
    res=None
    for Id in tab:
        if Id.code==code and Id.timeUTCRunTs>=ts :
            res=Id
            ts=Id.timeUTCRunTs
    return res

    



