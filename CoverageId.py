# coding: utf8
import requests
import string
import datetime
import time
import calendar
from xml.dom import minidom
from catalogueWCS import catalogueWCS
class CoverageId :
    def __init__(self, coverageId,resol):
        self.coverageId = coverageId  # le label renvoyé par la requête getCapabilities du WCS
        self.resol=resol  # la résolution ("001" ou "0025"), la même que celle fournie à la requête getCapabilities du WCS
        self.description=""  # description renvoyée par la requette getCapabilities du WCS
        for k,v in catalogueWCS.items():
            (nom,desc)=v
            if nom==self.chaineNom():
                self.code=k
                break
    def chaineNom (self):
        index=string.find(self.coverageId,"___");
        rep=self.coverageId[0:index];
        return rep
    def chaineDate(self):  # retourne la partie de l'Id indiquant la date du run
        index=string.find(self.coverageId,"___");
        rep=self.coverageId[index+3:index+23];
        rep=rep.replace(".",":")
        return rep
    def dateUTCRun(self):   # date UTC du RUN par decodage de chaineDate()
        chaine=self.chaineDate()
        rep=datetime.datetime.strptime(chaine,'%Y-%m-%dT%H:%M:%SZ')
        return rep
    def tsUTCRun(self):    # timestamp UTC du RUN
        date=self.dateUTCRun()
        return int(date.strftime('%s'))
    def ageRun(self):      # age du RUN en heures par différence à l'heure actuelle
        #ts = time.time()   
        ts= calendar.timegm(time.gmtime())
        return (ts-self.tsUTCRun())/60./60.
    def isCumul(self):    # le CoverageId concerne-t-il une donnée cumulée ou intégrée sur une durée ?
        index=string.find(self.coverageId,"Z_P")
        if (index<0):
            return False;
        else :
            return True;
    def cumul(self):   #  partie du CoverageId décrivant la durée du cumul
        if not self.isCumul():
            return ""
        else:
            index=string.find(self.coverageId,"Z_P")
            return (self.coverageId[index+3:len(self.coverageId)])
    def dureeCumul(self):  #  durée du cumul en secondes
        cumul=self.cumul()
        if cumul=="":
            return 0
        else:
            uniteDeTemps=cumul[len(cumul)-1:len(cumul)]
            if uniteDeTemps=="H":   #  il s'agit d'une durée exprimée en heures
                unit=3600
                nbUnite=cumul[1:len(cumul)-1]
            elif uniteDeTemps=="D":  # il s'agit d'une durée exprimée en jours
                unit=3600*24
                nbUnite=cumul[0:len(cumul)-1]
            nb=int(nbUnite)
            return nb*unit
    def describeCoveragePath(self) :  #calcul le path pour une requête describeCoverage pour ce CoverageID
        model="MF-NWP-HIGHRES-AROME-"+self.resol+"-FRANCE-WCS";
        path="https://geoservices.meteofrance.fr/services/"+model+"?SERVICE=WCS&version=2.0.1&REQUEST=DescribeCoverage&coverageID=";
        path=path+self.coverageId+"&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"; 
        return path
    def describeCoverage(self):  # envoi d'une requette describeCoverage pour ce CoverageId
        path = self.describeCoveragePath()
        status=-1
        while status != 200:
            r=requests.get(path)  # envoi d'une requête "describeCoverage" du WCS
            status=r.status_code
        fichier = open("WCSDescribeCoverage.xml","w")
        print >> fichier,r.content  # le résultat de la requête est un XML qui l'on écrit dans un ficheir
        fichier.close()
        res=self.analyseXML("WCSDescribeCoverage.xml")
        return res    # renvoi la liste des résultats
    def analyseXML(self,XMLFileName):
        mydoc = minidom.parse(XMLFileName)  # parse an XML file given by his name
        res={};  # le résultat de la requête sera mis dans un dictionnaire
        def getItems (tagName,code):
            #print (tagName)
            items = mydoc.getElementsByTagName(tagName) # recherches du tagName dans le ficheir XML parsé
            for i in range (0,len(items)):
                if (len(items[i].childNodes)>0):
                    val=items[i].childNodes[0].nodeValue
                else:
                    val=items[i].nodeValue
                #print val
                if len(items)>1:
                    complem=str(i)
                else:
                    complem=""
                if (val): res[code+complem]=val  # écriture de la valeur associée au tagName dans le dictionnire des résultats
        getItems ('swe:description',"descr")
        unit=mydoc.getElementsByTagName("swe:uom")[0].attributes.getNamedItem("code").nodeValue;
        res["descrUnite"]=unit
        getItems ('gmlrgrid:gridAxesSpanned',"axe")
        getItems ('gmlrgrid:coefficients',"axeCoeff")
        getItems ('gml:pos',"pos")
        getItems ('gml:low',"grilleLow")
        getItems ('gml:high',"grilleHigh")
        getItems ('gml:lowerCorner',"cornerLow")
        getItems ('gml:upperCorner',"cornerUpper")
        getItems ('gml:beginPosition',"timeDeb")
        getItems ('gml:endPosition',"timeFin")
        res["timeCumul"]=self.dureeCumul()
        res["timeTsDeb"]=self.tsUTCRun()
        res["Id"]=self.coverageId
        res["code"]=self.code
        return res    # renvoi le dictionnaire des résultats
        