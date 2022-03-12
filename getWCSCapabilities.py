import datetime
from Client_APIM_MF import Client_APIM_MF  
def getWCSCapabilities(modele,resol,domaine):
  """
  Envoi une requête getCapabilities au service WCS de MF et retourne la
  liste des coverageId disonibles
  """
  #import requests
  domaines=["FRANCE","EUROPE","GLOBE"]       # les domaines possibles
  assert domaine in domaines,domaine          
  resols=["001","0025","01","025"]           # les résolutions possibles
  assert resol in resols,resol              
  models=["HIGHRES-AROME","GLOBAL-ARPEGE"]   # les modèles MF possibles
  assert modele in models,modele
  modele_resol_domaine=f"{modele}-{resol}-{domaine}"
  print(modele_resol_domaine)
  combinaisons=["HIGHRES-AROME-001-FRANCE","HIGHRES-AROME-0025-FRANCE","GLOBAL-ARPEGE-01-EUROPE","GLOBAL-ARPEGE-025-GLOBE"]
  assert modele_resol_domaine in combinaisons , modele_resol_domaine
  #tok="eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJqcG1hY3ZlaWdoQGNhcmJvbi5zdXBlciIsImF1ZCI6IjY3QTU5Vk1jd0VCeUhTNmY3dHBVQWRfNmFfVWEiLCJuYmYiOjE2NDQzMjc5NDIsImF6cCI6IjY3QTU5Vk1jd0VCeUhTNmY3dHBVQWRfNmFfVWEiLCJzY29wZSI6ImFtX2FwcGxpY2F0aW9uX3Njb3BlIGRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvYW8xLW1mLm9yZzo5NDQzXC9vYXV0aDJcL3Rva2VuIiwiZXhwIjoxNjQ0MzMxNTQyLCJpYXQiOjE2NDQzMjc5NDIsImp0aSI6ImVlMjYwYzBjLTUxODktNDg4NC05NTVjLTAxMmExNDQ2ZDkyNCJ9.LIX69boro2nFW4eVh9Py1YHBp72_4AutxXcO44xNHSP26yaLtzedJ9EzLMFX1t2Lb6vT453ZAtUhjm36cwiQmBmNBviea4_xTA680UcLcE2k0G0vYFppe-VIKT1SuASmdpEQ-bbDiuSNOGuOXosTKoqhUG0biqDvyj-Y4pez757fhYzBLhpJgXRHawW_vIoLQfldBs1ippbXXct-OVZ5Q1mUeS7cAJNQr0nvLTf_TIYx07UvZCiQVN7t8ZxzCu1LN_USUBGdbrDdmvPbbBIsks38QVFOAK-TkLbvOPgW8QbnBtxJTtKSVZXVIF3MR8VwW1CkGUNiPungT95BLvsdmg"
  #path=f"https://geoservices.meteofrance.fr/services/MF-NWP-{modele_resol_domaine}-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"
  #path='https://public-api.meteofrance.fr/public/arome/1.0/wms/MF-NWP-HIGHRES-AROME-001-FRANCE-WMS/GetCapabilities?service=WMS&version=1.3.0'
  # path pour getCapabilities du WMS (Web Map Services) :
  #path=f"https://public-api.meteofrance.fr/public/arome/1.0/wms/MF-NWP-{modele_resol_domaine}-WMS/GetCapabilities?service=WMS&version=1.3.0"
  #path="https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCapabilities?SERVICE=WCS&VERSION=1.3.0&REQUEST=GetCapabilities"
  path=f"https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-{modele_resol_domaine}-WCS/GetCapabilities?SERVICE=WCS&VERSION=1.3.0&REQUEST=GetCapabilities"
  #path=f"https://geoservices.meteofrance.fr/services/MF-NWP-{modele_resol_domaine}-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJqcG1hY3ZlaWdoQGNhcmJvbi5zdXBlciIsImFwcGxpY2F0aW9uIjp7Im93bmVyIjoianBtYWN2ZWlnaCIsInRpZXJRdW90YVR5cGUiOm51bGwsInRpZXIiOiJVbmxpbWl0ZWQiLCJuYW1lIjoianBtdiIsImlkIjo2MDQsInV1aWQiOiJkOWFkNTZkMy00ZTU2LTRmY2QtYmE0ZC0xOWUzNWMzYTI0Y2EifSwiaXNzIjoiaHR0cHM6XC9cL3BvcnRhaWwtYXBpLm1ldGVvZnJhbmNlLmZyOjQ0M1wvb2F1dGgyXC90b2tlbiIsInRpZXJJbmZvIjp7IjUwUGVyTWluIjp7InRpZXJRdW90YVR5cGUiOiJyZXF1ZXN0Q291bnQiLCJncmFwaFFMTWF4Q29tcGxleGl0eSI6MCwiZ3JhcGhRTE1heERlcHRoIjowLCJzdG9wT25RdW90YVJlYWNoIjp0cnVlLCJzcGlrZUFycmVzdExpbWl0IjowLCJzcGlrZUFycmVzdFVuaXQiOiJzZWMifX0sImtleXR5cGUiOiJQUk9EVUNUSU9OIiwicGVybWl0dGVkUmVmZXJlciI6IiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6IkFST01FIiwiY29udGV4dCI6IlwvcHVibGljXC9hcm9tZVwvMS4wIiwicHVibGlzaGVyIjoiYWRtaW5fbWYiLCJ2ZXJzaW9uIjoiMS4wIiwic3Vic2NyaXB0aW9uVGllciI6IjUwUGVyTWluIn1dLCJleHAiOjE3Mzg5MDYxNTUsInBlcm1pdHRlZElQIjoiIiwiaWF0IjoxNjQ0Mjk4MTU1LCJqdGkiOiI0NjVmOTg5ZC1lZGI4LTQ1NmYtYmRlMi1iZGZkOWVkMTc2YTMifQ==.r5ee2shK0_CqmAoHskiY_3M44owRWrOJBPQZJQmB-ELjxuttujjEfKINmcXX6GV4rh9kMLY9f-PWfZ--L1NhTPZThwluJRQwWyEjo_L1krsELuw1Gibb00ABhH8EmLTSrKlnaL4LbdAsPERbNA6Q9Dkoh0Blf0iWrSIoL8xOLRm8PFuoE0smVOxLiJOEebxtIQJbIs7aN7j2gTPyxCtt_KIQgEbZKoQyv39FdbHaeb5jFtYQ-sShHNbNdl7LDZl0bQLWQjIkn23PIJvld5aOP5VqJ5W10ITrMM9JEJt9cbjwA4AbdipUSfz_nldzN5JcKkndKO3REVTgzyPQPq3iVg=="
  #path=f"https://geoservices.meteofrance.fr/services/MF-NWP-{modele_resol_domaine}-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token={tok}"

  print(path)
  #rep=requests.get(path)   # requête GetCapabilities du standard Web Coverage Services (WCS)
  rep=Client_APIM_MF().request("GET",path,verify=False)   # requête GetCapabilities du standard Web Coverage Services (WCS)
  assert rep.status_code == 200 , rep.status_code
  from xml.dom.minidom import parseString  # analyse du XML retourné par la requête GetCapabilities
  dom = parseString(rep.content)
  items = dom.getElementsByTagName('wcs:CoverageId')
  rep={}
  rep["now_utc"]=str(datetime.datetime.utcnow())
  rep["modele"]=modele
  rep["resolution"]=resol
  rep["domaine"]=domaine
  res=[];
  lesTitres=set()
  cle={}
  for i in range (0,len(items)):  # boucle sur les CoverageId trouvés dans le fichier XML parsé
      coverageId=items[i].childNodes[0].nodeValue  # le coverageId
      node=items[i].parentNode
      node=node.getElementsByTagName('ows:Title')  # recherche de sa description
      description=node[0].childNodes[0].nodeValue  # sa description
      #print (coverageId,description)
      run=coverageId.split("__")[-1][1:]
      res.append({"Id":coverageId,"desc":description,"run":run})
      #cle='"",("'+CoverageId(coverageId,resol).chaineNom()+'","'+description+'"),'
      #lesTitres.add(cle)
      #cov=CoverageId(coverageId,resol)  # création dun objet CoverageId
      #cov.descr=description  # renseignement de sa descritpion
      #res.append(cov)  # écriture des objets CoverageId dans la liste des résultats
  titres=sorted(lesTitres)
  print(len(res))
  rep["nb_ID"]=len(res)
  rep["lesID"]=res
  return rep