#coding: utf8
import datetime
import calendar
import time
import math
def chaineUTCFromTs(tsUTC):  # chaine de date au format '%Y-%m-%dT%H:%M:%SZ' à partir d'un timestamp
    return datetime.datetime.utcfromtimestamp(tsUTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def tsNow():
    #return calendar.timegm(time.gmtime())  # now
    return time.time()  # now
def nextChainesPrevi():  # renvoi les 48 prochaines heures rondes UTC
    ts= tsNow()  # now
    rep=[]
    #rep.append(chaineUTCFromTs(ts))
    for i in range(0,48):
        ts=ts+3600-(ts % 3600)  #  on ajoute 3600 secondes et on arrondi à l'heure ronde précèdante
        rep.append(chaineUTCFromTs(ts))
    return rep   #  tableau des chaines
def laNextChainePrevi():  # renvoi la première heure ronde qui suit l'heure UTC actuelle
    return nextChainesPrevi()[0]
def lesChainesDateEntourantes():  # renvoi la précédante et la prochaine heure ronde UTC et la distance dans [0,100] à la précedante
    ts= tsNow()  # now
    tsAfter=ts+3600-(ts % 3600)  #  on ajoute 3600 secondes et on arrondi à l'heure ronde précèdante
    tsBefore=tsAfter-3600  # on retranche une heure
    dist=(ts-tsBefore)/(3600.)*100.
    chaineBefore=chaineUTCFromTs(tsBefore)
    chaineAfter=chaineUTCFromTs(tsAfter)
    return (chaineBefore,chaineAfter,dist)
def vLat(v):  # vitesse méridienne (deg/unité de temps) en fonction de la vitesse méridienne (m/unité de temps)
    R=6371000. # rayon de la terre (m)
    circonf=R*2.*math.pi
    return v/circonf*360.
def uLng (u,phi):  # vitesse zonale (deg/unité de temps) en fonction de la vitesse zonale (m/unité de temps) et de la latitude phi (degrés)
    if not(-90.< phi <90.): raise Exception ("uLng: phi doit être dans ]-90.,90.[")
    return vLat(u)/math.cos(phi*math.pi/180.)  # on divise par le cosinus de la latitude
def getHeureLocale(heureUTC, longi):
    # calcul du décalage horaire géographique par rapport à Greenwich
    if not (-180<=longi<=180.): raise Exception ("heureLocale : longi incorrecte")
    locale = heureUTC+12.*longi/180.
    if locale>24. : locale=locale-24
    if locale<0. : locale=locale+24
    return locale

#print getHeureLocale(5.0,+3.)
#print (tsNow());