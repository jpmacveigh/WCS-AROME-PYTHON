import datetime
from getProfiVerticalMeteociel import getProfilVerticalMeteoCiel

def getNowMeteociel(code_param,lati,longi,alti):
  ts_now= datetime.datetime.timestamp(datetime.datetime.now())
  print(ts_now)
  for ech in [6,9,12]:
    res=getProfilVerticalMeteoCiel(ech,lati,longi,[alti])
    print (res["UTC_previ_string"],res["ts_previ"],res["altitudes_interpolees"][0][code_param])
    print (ts_now>=res["ts_previ"])


getNowMeteociel("temp",50.6,3.06,9500)
