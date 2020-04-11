import datetime
import numpy as np
from getProfiVerticalMeteociel import getProfilVerticalMeteoCiel

def getNowMeteociel(code_param,lati,longi,alti): 
  ''' renvoit la valeur actuelle pour le "code_param" à une position et altitude (m) données.
  La valeur retournée est interpolée verticalement et dans le temps '''
  ts_now= datetime.datetime.timestamp(datetime.datetime.now())
  print(ts_now)
  ts=[]
  val=[]
  for ech in [3,6,9]:
    res=getProfilVerticalMeteoCiel(ech,lati,longi,[alti])
    ts.append(res["ts_previ"])
    val.append(res["altitudes_interpolees"][0][code_param])
    print (res["UTC_previ_string"],res["ts_previ"],res["altitudes_interpolees"][0][code_param])
    print (ts_now>=res["ts_previ"])
    if (res["ts_previ"]>ts_now) : break  # si la secode prevision est plus tardive que now
  res=np.interp(ts_now,ts,val)   #  interpolation temporelle (sur 2 ou trois valeurs)
  print (res)

getNowMeteociel("temp",50.6,3.06,5000)
