import datetime
def next_hh_UTC(hh_UTC):
  ''' renvoi la prochaine HH [0,23] heure UTC '''
  tsnow=datetime.datetime.utcnow().timestamp()  # quelle heure UTC est-il ?
  #print (tsnow)
  date_now=datetime.datetime.utcfromtimestamp(tsnow)
  #print(date_now)
  ts_date_hh_UTC=date_now.replace(hour=hh_UTC,minute=0,second=0,microsecond=0).timestamp() # on se place à hh_UTC
  if (ts_date_hh_UTC) < tsnow : ts_date_hh_UTC=ts_date_hh_UTC+86400 # si c'est déja passé, on prend celle de demain
  return (ts_date_hh_UTC,datetime.datetime.utcfromtimestamp(ts_date_hh_UTC))

#print(next_hh_UTC(4))