#coding: utf8
import json
import sqlite3
import requests
import arrow
import math
import sys
import datetime
from getWCSCapabilities import profilVertical
from getWCSCapabilities import mostRecentId
from getWCSCapabilities import prevision
from AxeVertical import AxeVertical
sys.path.insert(0, '/home/ubuntu/workspace/Utils') # insérer dans sys.path le dossier contenant le/les modules
from Utils import *
class Vehicule:  # un véhicule qui se déplace
    def __init__(self,lat,lng,alt):
        if not(-180.<=lng<=180.): raise Exception ("Vehicule : lng doit être dans [-180,+180]")
        if not(-90.<=lat<=90.): raise Exception ("Vehicule : lat doit être dans [-90,+90]")
        if not(alt>=0.): raise Exception ("Vehicule : alt être >= 0.")
        self.lng=lng
        self.lat=lat
        self.alt=alt
        self.getTimeZone()   #  la timezone du lieu
        self.getSunRiseSunSet()  #  détermination heures locales de lever et de coucher du soleil du lieu du véhicule
        self.getHauteur()  #  aquisition de la hauteur en fonction de l'heure
        self.getVille()  # recherche du nom de la ville qui est en dessous
        self.initDB()
    def getTime(self):  # Quelle heure UTC est-il ?
        self.heureUTC=arrow.utcnow()
        self.tsUTC=self.heureUTC.timestamp;
        #print ("heure UTC: "+str(self.heureUTC)+"  soit TS: "+str(self.tsUTC))
        #print ("heure locale Paris: "+str(self.heureUTC.to("Europe/Paris")))  # heure de Paris
    def getTimeZone(self):  #  Dans quel fuseau horaire suis-je ?
        self.getTime();
        urlGetTZ="https://maps.googleapis.com/maps/api/timezone/json?location="+str(self.lat)+","+str(self.lng)+"&timestamp="+str(self.tsUTC)+"&key=AIzaSyAJ5k6nijmVsFGQ8EqVs4YiSkdDucJbJ2s"
        status=0
        while status != 200:
            r=requests.get(urlGetTZ)
            status=r.status_code
        #print r.content  # le résultat de la requête
        # tester :  http://api.timezonedb.com/v2.1/get-time-zone?key=TE4GPIYXBN1Y&format=json&by=position&lat=50.6&lng=3.06&time=1552207312
        # tester :  http://api.geonames.org/timezoneJSON?lat=49.11&lng=-27.82&username=demo
        self.timeZone=json.loads(r.content)
        if (self.timeZone["status"]=="ZERO_RESULTS"): raise Exception ("Vehicule : timeZone inconnu de Google")
        #print self.timeZone["timeZoneId"]
        self.heureLocale=self.heureUTC.to(self.timeZone["timeZoneId"])
        #print ("heure locale du lieu: "+str(self.heureLocale))
    def getSunRiseSunSet(self):  # heures locales de lever et de coucher du soleil
        url="https://api.sunrise-sunset.org/json?lat="+str(self.lat)+"&lng="+str(self.lng)+"&date=today&formatted=0"
        #print url
        status=0
        while status != 200:
            r=requests.get(url,verify=False)
            status=r.status_code
        #print r.content  # le résultat de la requête
        self.sunRiseSunSet=json.loads(r.content)
        sunrise=arrow.get(self.sunRiseSunSet["results"]["sunrise"])
        self.heureSunriseLocale=sunrise.to(self.timeZone["timeZoneId"])
        if (self.heureSunriseLocale.day!=self.heureLocale.day):
            self.heureSunriseLocale=self.heureSunriseLocale.replace(day=self.heureLocale.day)
        #print sunrise
        self.tsSunriseUTC=self.heureSunriseLocale.timestamp
        #print sunrise.to(self.timeZone["timeZoneId"])
        sunset=arrow.get(self.sunRiseSunSet["results"]["sunset"])
        #print sunset
        self.heureSunsetLocale=sunset.to(self.timeZone["timeZoneId"])
        if (self.heureSunsetLocale.day!=self.heureLocale.day):
            self.heureSunsetLocale=self.heureSunsetLocale.replace(day=self.heureLocale.day)       
        self.tsSunsetUTC=self.heureSunsetLocale.timestamp
        self.dayPosition=(self.tsUTC-self.tsSunriseUTC)/1./self.sunRiseSunSet["results"]["day_length"]*100.  # Où en est-on de la journée dans [0%,100%]
        if self.dayPosition <0.:
            self.dayPhase="night morning"
        elif 0<=self.dayPosition <50.:
            self.dayPhase="day morning"
        elif 50<=self.dayPosition <=100.:
            self.dayPhase="day afternoon"
        else :
           self.dayPhase="night evening" 
    def getHauteur(self):   # calcul l'altitude du véhicule en fonction de l'heure locale
        hautNuit=10.
        if 0<=self.dayPosition <=100.:
            hautMidi=3000.
            x=(self.dayPosition/100.*2.*math.pi)-(math.pi/2.)
            self.hauteur=((math.sin(x)+1.)*0.5*(hautMidi-hautNuit))+hautNuit
        else:
            self.hauteur=hautNuit
    def moove (self,u,v,dt) : # le déplace pendant dt unités de temps avec les vitesses zonale et méridienne (u,v) en m/unité de temps
        self.lat=self.lat+vLat(v)*dt           # la latitude varie en fonction de v (vitesse méridienne)
        self.lng=self.lng+uLng(u,self.lat)*dt  # la longitude varie en fonction de u (vitesse zonale)
    def getVentActuel (self):   #  Aquisition du vent Arome 0025 actuel à la hauteur du véhicule
        lesDeuxDates=lesChainesDateEntourantes()
        IdU=mostRecentId("0025","U(h)")    #  composante zonale du vent (positive vers l'Est)
        IdU.describeCoverage()
        #print IdU.height
        lesDeuxHauteurs=AxeVertical(IdU.height).encadrement(self.hauteur)
        #print (lesDeuxDates,self.haut,lesDeuxHauteurs)
        uBasBefore=prevision (IdU,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[0])
        uBasAfter =prevision (IdU,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[0])
        uBas=(uBasBefore*(100.-lesDeuxDates[2])+lesDeuxDates[2]*uBasAfter)/100.     #  interpolation temporelle
        #print uBasBefore,uBasAfter,uBas
        uHautBefore=prevision (IdU,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[1])
        uHautAfter =prevision (IdU,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[1])
        uHaut=(uHautBefore*(100.-lesDeuxDates[2])+lesDeuxDates[2]*uHautAfter)/100.  #  interpolation temporelle
        #print uHautBefore,uHautAfter,uHaut
        u=(uBas*(100.-lesDeuxHauteurs[2])+lesDeuxHauteurs[2]*uHaut)/100.  # interpolation verticale
        #print uBas,uHaut,u
        IdV=mostRecentId("0025","V(h)")   #  composante méridienne du vent
        IdV.describeCoverage()
        vBasBefore=prevision (IdV,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[0])
        vBasAfter =prevision (IdV,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[0])
        vBas=(vBasBefore*(100.-lesDeuxDates[2])+lesDeuxDates[2])*vBasAfter/100.  #  interpolation temporelle
        #print vBasBefore,vBasAfter,vBas
        vHautBefore=prevision (IdV,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[1])
        vHautAfter =prevision (IdV,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[1])
        vHaut=(vHautBefore*(100.-lesDeuxDates[2])+lesDeuxDates[2])*vHautAfter/100.  #  interpolation temporelle
        #print vHautBefore,vHautAfter,vHaut
        v=(vBas*(100.-lesDeuxHauteurs[2])+lesDeuxHauteurs[2]*vHaut)/100.  # interpolation verticale
        #print vBas,vHaut,v
        print (u,v)
        return (u,v)
    def getVille(self):   # détermination de la villeau dessus de laquelle est le véhicule
        path="https://nominatim.openstreetmap.org/reverse?format=json&lat="+str(self.lat)+"&lon="+str(self.lng)+"&zoom=18&addressdetails=1"
        print path
        status=0
        while status != 200:
            r=requests.get(path,verify=False)
            status=r.status_code
        #print r.content  # le résultat de la requête
        self.localisation=json.loads(r.content)
        self.ville=self.localisation["display_name"]
        return self.ville
    def initDB(self):
        self.conn = sqlite3.connect('traject.sqlite')
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS trajectoire (ts num,lat real,lng real,haut real,lieu text)")
    def savePosition(self):
        sql="INSERT INTO trajectoire VALUES ("
        sql=sql+str(self.tsUTC)
        sql=sql+","+str(self.lat)+","+str(self.lng)+","+str(self.hauteur)+","
        sql=sql+'"'+self.ville+'")'
        #print sql
        c=self.conn.cursor()
        #c.execute("INSERT INTO trajectoire VALUES (150.,50.6,3.06,22.0,'Lille')")
        c.execute(sql)
        self.conn.commit()
    def listPositions(self):
        c=self.conn.cursor()
        for row in c.execute("SELECT * FROM trajectoire"):
            print row
    def affiche(self):
        for k in sorted(self.__dict__.keys()):
            print (k+":  "+str(self.__dict__[k]))
"""
v=Vehicule (13.6,103.06,20.)    # Vietnam
v.affiche()
v=Vehicule (50.6,3.06,20.)      # Lille
v.affiche()
v=Vehicule (-22.26,166.15,20.)  # Nouméa
v.affiche()
v=Vehicule (-17.54,-149.57,20.) # Papeete
v.affiche()
"""
#reso="0025"
from time import sleep

#v.savePosition()
#v.listPositions()
"""
#v=Vehicule(51.77433177319676,3.862306215709615,200)
#v=Vehicule (-22.26,166.15,20.)  # Nouméa

"""
v=Vehicule (50.635472,3.055083,20.)      # Lille
print str(datetime.datetime.now())
print v.ville
v.savePosition()
v.listPositions()
dt=300. # interval d'itération en secondes
for i in range(100):
    sleep(dt)    #in seconds
    print i,str(datetime.datetime.now())
    vent=v.getVentActuel()
    v.moove(vent[0],vent[1],dt)
    v=Vehicule(v.lat,v.lng,v.hauteur)
    v.savePosition()
    v.listPositions()
    print v.ville
"""
tab=profilVertical (reso,"U(h)",3.06,50.6)
print (json.dumps(tab,indent=4,sort_keys=True))
tab=profilVertical (reso,"V(h)",3.06,50.6)
print (json.dumps(tab,indent=4,sort_keys=True))

print v.dayPhase,v.dayPosition,v.haut,v.lat,v.lng
v.moove(5,5,3600)
print v.dayPhase,v.dayPosition,v.haut,v.lat,v.lng
"""