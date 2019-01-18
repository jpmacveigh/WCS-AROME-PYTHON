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
        self.descr=""  # description renvoyée par la requette getCapabilities du WCS
        self.code=""
        for k,v in catalogueWCS.items():
            (nom,desc)=v
            if nom==self.chaineNom():
                self.code=k
                break
        if self.code=="":
            raise Exception (self.chaineNom() + " non trouvee dans le dictionnaire"  +self.descr)
        self.timeUTCRun=self.chaineDate()
        self.timeUTCRunTs=self.tsUTCRun()
        self.timeDeb=""
        self.timeFin=""
    def chaineNom (self):
        index=string.find(self.coverageId,"___");
        rep=self.coverageId[0:index];
        return rep
    def chaineDate(self):  # retourne la partie de l'Id indiquant la date du run sous un format du type : "2019-01-13T13:00:00Z"
        index=string.find(self.coverageId,"___");
        rep=self.coverageId[index+3:index+23];
        rep=rep.replace(".",":")
        return rep
    def dateUTCRun(self):   # date UTC du RUN par decodage de chaineDate()
        chaine=self.chaineDate()
        return self.dateFromChaine(chaine)
    def dateFromChaine(self,chaine):  #  objet date à partir d'une chaine du type : "2019-01-13T13:00:00Z"
        rep=datetime.datetime.strptime(chaine,'%Y-%m-%dT%H:%M:%SZ')
        return rep
    def tsUTCRun(self):    # timestamp UTC du RUN
        dateUTC=self.dateUTCRun()
        return self.ts(dateUTC)
    def ts(self,dateUTC):  #  timestamp d'une date UTC
        return int(dateUTC.strftime('%s'))
    def chaineUTCFromTs(self,tsUTC):  # chaine de date au format '%Y-%m-%dT%H:%M:%SZ' à partir d'un timestamp
        rep=datetime.datetime.utcfromtimestamp(tsUTC).strftime('%Y-%m-%dT%H:%M:%SZ')
        return rep
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
    def describeCoverage(self):  # Envoi et traitement d'une requette describeCoverage pour ce CoverageId
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
                if (val):
                    self.__dict__[code+complem]=val
                    res[code+complem]=val  # écriture de la valeur associée au tagName dans le dictionnire des résultats
        getItems ('swe:description',"descr")
        unit=mydoc.getElementsByTagName("swe:uom")[0].attributes.getNamedItem("code").nodeValue
        res["descrUnite"]=unit
        self.unite=unit
        #gmlrgrid:offsetVector srsDimension="4"
        dim=mydoc.getElementsByTagName("gmlrgrid:offsetVector")[0].attributes.getNamedItem("srsDimension").nodeValue
        self.dim=int(dim)   # nombre d'axes (dimensions) du coverageId
        getItems ('gmlrgrid:gridAxesSpanned',"axe")
        getItems ('gmlrgrid:coefficients',"axeCoeff")
        getItems ('gml:pos',"pos")
        getItems ('gml:low',"grilleLow")
        getItems ('gml:high',"grilleHigh")
        getItems ('gml:lowerCorner',"cornerLow")
        getItems ('gml:upperCorner',"cornerUpper")
        getItems ('gml:beginPosition',"timeDeb")
        self.timeDebTs=self.ts(self.dateFromChaine(self.timeDeb))
        getItems ('gml:endPosition',"timeFin")
        self.timeFinTs=self.ts(self.dateFromChaine(self.timeFin))
        res["timeCumul"]=self.dureeCumul()
        self.timeCumul=self.dureeCumul()
        res["timeTsUTCRun"]=self.tsUTCRun()
        res["Id"]=self.coverageId
        self.Id=self.coverageId
        res["code"]=self.code
        self.code=self.code
        for cle in self.__dict__:  # découpage des coefficients des axes et mise dans un tableau
            if "Coeff" in cle:
                val=self.__dict__[cle]
                val=list(map(lambda x: int(x), val.split()))
                self.__dict__[cle]=val
        if self.dim==3 :    # contôle cohérence timeDeb, timeFin et axe des temps
            axeTime="axeCoeff2"
            self.niv=None
        else:  #  cas où dim= 4 et où il y a un niveau vertical
            axeTime="axeCoeff3"
            axeNiv="axeCoeff2"
            self.niv=self.__dict__["axe2"]
            self.__dict__[self.niv]=self.__dict__[axeNiv]
            del self.__dict__[axeNiv]
        self.time=self.__dict__[axeTime]  #  renommage de l'axe des temps
        del self.__dict__[axeTime]
        tab=[]
        for ts in self.time:  # Ajout des dates des prévisions
            tsPrevi=self.timeUTCRunTs+ts
            chainePrevi=self.chaineUTCFromTs(tsPrevi)
            tab.append(chainePrevi)
        self.timeDatePrevi=tab
        self.timeNbEch=len(self.time)  # nombre d'échéance temporelles dasn le CoverageId
        tsFin=self.timeUTCRunTs+self.time[-1]
        if tsFin != self.timeFinTs :
            print self.timeDeb
            print self.timeDebTs
            print self.time[-1]
            print tsFin
            print self.timeFin
            print self.timeFinTs
            raise Exception ("Erreur timeFinTs")
        tsDeb=self.timeUTCRunTs+self.time[0]
        if tsDeb != self.timeDebTs : raise Exception ("Erreur timeDebTs")
        return res    # renvoi le dictionnaire des résultats
    def niveau(self,numNiv):  #  renvoi la valeur du "numNiv" -ième niveau 
        if numNiv<0 or numNiv> len(self.__dict__[self.niv]):
            raise Exception ("Numéro de niveau non valide: %s" % numNiv)
        return self.__dict__[self.niv][numNiv]
    def getCoverage(self,latiSud,latiNord,longiOuest,longiEst,chaineDatePrevi,niv=None):
        """ https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__
         /MF-NWP-HIGHRES-AROME-0025-FRANCE-WCS?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage
         &format=image/tiff&coverageId=GEOPOTENTIAL__ISOBARIC_SURFACE___2017-08-29T06.00.00Z
         &subset=lat(50.0,51.0)&subset=long(3.0,4.0)&subset=pressure(100)&subset=time(2017-08-29T15:00:00Z)"""
        
        path="https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__/MF-NWP-HIGHRES-AROME-";
        path=path+self.resol+"-FRANCE-WCS?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId=";
        path=path+self.coverageId
        latitude  = "&subset=lat("+str(latiSud)+","+str(latiNord)+")"
        longitude = "&subset=long("+str(longiOuest)+","+str(longiEst)+")";
        path=path+latitude+longitude
        if niv: path=path+"&subset="+self.niv+"("+str(niv)+")"  # ajout du niveau, if any
        path=path+"&subset=time("+chaineDatePrevi+")"
        print path
        status=-1
        while status != 200:
            r=requests.get(path)  # envoi d'une requête "getCoverage" du WCS
            status=r.status_code
        fichier = open("WCSgetCoverage.tif","w")
        print >> fichier,r.content  # le résultat de la requête est un geotiff que l'on écrit dans un ficheir
        fichier.close()