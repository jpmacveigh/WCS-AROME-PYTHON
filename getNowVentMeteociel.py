import datetime
import numpy as np
from getProfiVerticalMeteociel import getProfilVerticalMeteoCiel
from VentHorizontal import VentHorizontal

def getNowVentMeteociel(lati,longi,alti): 
  ''' renvoit la valeur actuelle pour du vent (u,v)(m/s) à une position et altitude (m) données.
  Les valeurs retournées sont interpolées verticalement et dans le temps '''
  ts_now= datetime.datetime.timestamp(datetime.datetime.now())
  #print(ts_now)
  ts=[]
  les_u=[]
  les_v=[]
  nb_ech=0
  for ech in [3,6,9]:
    res=getProfilVerticalMeteoCiel(ech,lati,longi,[alti])
    ts.append(res["ts_previ"])
    les_u.append(res["altitudes_interpolees"][0]["u"])
    les_v.append(res["altitudes_interpolees"][0]["v"])
    #print (res["UTC_previ_string"],res["ts_previ"],res["altitudes_interpolees"][0]["u"],res["altitudes_interpolees"][0]["v"])
    #print (ts_now>=res["ts_previ"])
    nb_ech +=1
    if (res["ts_previ"]>ts_now) : break  # si la secode prevision est plus tardive que now, on ignore la troisième
  u=np.interp(ts_now,ts,les_u)  #  interpolation temporelle (sur 2 ou trois valeurs)
  v=np.interp(ts_now,ts,les_v)
  return (u,v,VentHorizontal(u,v).toStringKmh(),nb_ech)

print(getNowVentMeteociel(50.6,3.06,384))
