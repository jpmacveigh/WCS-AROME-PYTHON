# coding: utf8
from __future__ import unicode_literals
import requests
import sys
import time
import calendar
import os
sys.path.insert(0, '/home/ubuntu/workspace/Utils') # insérer dans sys.path le dossier contenant le/les modules
sys.path.insert(0, '/home/ubuntu/environment/node_jpmv/Utils') # insérer dans sys.path le dossier contenant le/les modules
from Utils import lesChainesDateEntourantes
from Utils import chaineUTCFromTs
from CoverageId import CoverageId
#import xml.etree.ElementTree as ET
from xml.dom import minidom
def getWCSCapabilities(resol):  # Lance une requête "getCapabilities" du WCS pour le modèel Arome de MF. La résolution ("0025" ou "001") est donnée en paramètre. 
    XMLFileName="WCSCapabilities.xml"
    #  on regarde si la dernière requête "getCapabilities" n'est trop récente
    now=time.time()
    if (not ((os.path.exists(XMLFileName) and (now-os.path.getctime(XMLFileName)<=10*60)))): #  plus de 10 minutes ?
        path="https://geoservices.meteofrance.fr/services/MF-NWP-HIGHRES-AROME-"
        path=path+resol+"-FRANCE-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"
        #curl "https://geoservices.meteofrance.fr/services/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__" > resultGetCapabilities
        status=-1
        while status != 200:
            r=requests.get(path)
            status=r.status_code
        fichier = open(XMLFileName,"w")
        print >> fichier,r.content  # le résultat de la requête est un XML qui l'on écrite dans un ficheir
        fichier.close()
    mydoc = minidom.parse(XMLFileName)  # parse an XML file given by his name
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

def mostRecentId(resol,code):   # renvoi le plus récent des CoverageId de resolution "resol" et dont le code du la variable est "code"
    tab=getWCSCapabilities(resol)   #  envoi d'ue requête getCapabilities au WCS pour la résolution "resol"
    ts=-sys.maxint-1    #  le plus grand des entiers
    res=None
    for Id in tab:    #  recherche du plus récent run pour le paramètre de code "code"
        if Id.code==code and Id.timeUTCRunTs>=ts :  #  on lit le timestamp du run
            res=Id
            ts=Id.timeUTCRunTs
    return res
def profilVertical(resol,code,longi,lati):   #  renvoi le profil vertical à l'heure précedante
    Id=mostRecentId(resol,code)
    if Id:
        res={}
        Id.describeCoverage()
        if (Id.dim!=4): raise Exception ("profilVertical : %s n'est pas de dimension 4" %(code))
        #print (Id.code,Id.descr,Id.niv)
        chaineDate=lesChainesDateEntourantes()[0]
        res["titre"]="Profil vertical"
        res["code"]=Id.code
        res["descr"]=Id.descr
        res["vertical"]=Id.niv
        res["run"]=Id.chaineDate()
        res["previ"]=chaineDate
        res["unit"]=Id.unite
        res["niveaux"]=[]
        res["position"]={"longitude":longi,"latitude":lati}
        niveaux=Id.__dict__[Id.niv]
        res["nbNiv"]=len(niveaux);
        #print niveaux
        for niv in niveaux:
            #Id.getCoverage(lati-.1,lati+.1,longi-.1,longi+.1,Id.timeDatePrevi[0],niv)
            Id.getCoverage(lati-.1,lati+.1,longi-.1,longi+.1,chaineDate,niv)
            #print niv,Id.valeur(longi,lati)
            res["niveaux"].append({"niveau":niv,"valeur":Id.valeur(longi,lati)})
        ts= calendar.timegm(time.gmtime())
        res["now"]=chaineUTCFromTs(ts)
        return res
    else : return None

def previsions (resol,code,longi,lati,niveau=None): 
    if not(niveau==None): niveau = int(niveau)
    Id=mostRecentId(resol,code)
    if Id:
        res={};
        Id.describeCoverage();
        if Id.dim==4 and niveau==None : # Cas où il manque le niveau
            return {"error":"Previsions : Le champs est de dim=4, le niveau est manquant"};
        if Id.dim==3 and not(niveau==None): # Cas où le niveau n'est pas requis
            return {"error":"Previsions : Le champs est de dim=3, le niveau n'est pas requi"};  
        res={};
        res["titre"]="Previsions"
        res["code"]=Id.code
        res["descr"]=Id.descr
        res["niveau"]=niveau
        res["run"]=Id.chaineDate()
        res["unit"]=Id.unite
        res["position"]={"longitude":longi,"latitude":lati}
        res["previsions"]=[]
        res["nbPrevi"]= len(Id.timeDatePrevi);
        for date in Id.timeDatePrevi:
            #Id.getCoverage(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau)
            previ=prevision(Id,longi,lati,date,niveau)
            res["previsions"].append({"date":date,"valeur":previ})
        return res;
    return {"error":"Previsions : mostRecentId was not found : Check the given code"};
def prevision (Id,longi,lati,date,niveau=None):
    if Id.dim==4 and niveau==None : # Cas où il manque le niveau
        raise Exception ("prevision : Le champs est de dim=4, le niveau est manquant");
    if Id.dim==3 and not(niveau==None): # Cas où le niveau n'est pas requis
        raise Exception ("prevision : Le champs est de dim=3, le niveau n'est pas requi");  
    Id.getCoverage(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau)
    return Id.valeur(longi,lati)