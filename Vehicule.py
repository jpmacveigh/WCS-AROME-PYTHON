#coding: utf8
import json
import requests
import arrow
class Vehicule:  # un véhicule qui se déplace
    def __init__(self,lat,lng,alt):
        if not(-180.<=lng<=180.): raise Exception ("Vehicule : lng doit être dans [-180,+180]")
        if not(-90.<=lat<=90.): raise Exception ("Vehicule : lat doit être dans [-90,+90]")
        if not(alt>=0.): raise Exception ("Vehicule : alt être >= 0.")
        self.lng=lng
        self.lat=lat
        self.alt=alt
        self.getTimeZone()
        self.getSunRiseSunSet()
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
        if (self.tsSunriseUTC<=self.tsUTC<=self.tsSunsetUTC):  # Fait-il jour ou nuit ?
            self.dayPhase="day"
        else:
            self.dayPhase="night"
        self.dayPosition=(self.tsUTC-self.tsSunriseUTC)/1./self.sunRiseSunSet["results"]["day_length"]*100.  # Où en est-on de la journée dans [0%,100%]
    def affiche(self):
        for k in sorted(self.__dict__.keys()):
            print (k+":  "+str(self.__dict__[k]))

#v=Vehicule (13.6,103.06,20.)    # Vietnam
#v=Vehicule (50.6,3.06,20.)       # Lille
#v=Vehicule (-22.26,166.15,20.)  # Nouméa
v=Vehicule (-17.54,-149.57,20.)  # Papeete
v.affiche()
