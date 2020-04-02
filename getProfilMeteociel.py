import requests
import bs4 as BeautifulSoup
import numpy as np
from VentHorizontal_DDFF import VentHorizontal_DDFF
import json
import datetime
def getProfilVerticalMeteoCiel ():
        ''' Extraction du profil vertical de vent d'une page HTML fournie par Météociel
            voir : http://www.meteociel.fr/modeles/sondage_gfs.php             '''
        result={}
        # url pour modèle GFS 0.25° à Lille
        url ="http://www.meteociel.fr/modeles/sondage2.php?archive=0&ech=36&map=2&runpara=0&x1=3.07585&lat=50.6288&lon=3.07585&userlat=1&y1=50.6288"
        codes_vent=["nne","ne","ene","e","ese","se","sse","s","sso","so","oso","o","ono","no","nno","n"]
        dic_vent={}
        i=1
        for code in codes_vent:
            dic_vent[code]=i*22.5   # rose de 16 valeurs pour 360 degrès
            i=i+1
        status=0
        while status != 200:
            r=requests.get(url)
            status=r.status_code
            #print (status)
        res=r.content
        soup=BeautifulSoup.BeautifulSoup(res,"lxml")
        tables=[]
        for p in soup.find_all('table'):  #  on extrait toutes les tables de la page HTML
            tables.append(p)
        num_row=0
        for row in tables[0].find_all('tr'):   # la premiere table est celle des données générales du profil
            colonnes=row.find_all('td')
            if num_row==0:
                 for colonne in colonnes:
                    col_run=colonne.text      # la définition du run du modèle
                    result["col_run"]=col_run     
                    split=col_run.split()
                    result["an_run"]=int(split[-1])
                    result["mois_run"]=split[-2]
                    mois=["janvier","fevrier","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","decembre"]
                    result["num_mois_run"]=mois.index(result["mois_run"])+1
                    assert 1<=result["num_mois_run"]<=12 , result["num_mois_run"]
                    result["jour_run"]=int(split[-3])
                    result["heure_run"]=int(split[2][:-1])
                    result["date_run"]=datetime.datetime(result["an_run"],result["num_mois_run"],result["jour_run"],result["heure_run"])
                    
            else:
                 num_col=0
                 for colonne in colonnes:
                    if num_col==0:
                        col_isos=colonne.text  # les isothermes 0°C, -10°C et -20°C
                        n=col_isos.find("|")
                        result["iso_0"]=float(col_isos[0:n])
                        col_isos=col_isos[n+1:]
                        n=col_isos.find("|")
                        result["iso_M10"]=float(col_isos[0:n])
                        col_isos=col_isos[n+1:]
                        result["iso_M20"]=float(col_isos)
                    else:
                        col_date=colonne.text  # la date et l'échéance des prévision
                        result["col_date"]=col_date   # A finir
                        ndeb=col_date.find("(+")
                        nfin=col_date.find("h)")
                        result["echeance"]=int(col_date[ndeb+2:nfin])
                        result["date_previ"]=result["date_run"]+datetime.timedelta(hours=result["echeance"])
                    num_col=num_col+1
            num_row=num_row+1
        result["niveaux"]=[]
        num_row=0
        for row in tables[1].find_all('tr'):# la seconde table de la page est celle des valeurs numérique du profil vertical
            if num_row > 0:                          # on saute la première ligne de la table
                colonnes=row.find_all('td')          # on récupère les colonnes de chaque ligne de la table
                alti=float(colonnes[0].text[:-2])    # la première colonne donne l'altitude (m)
                press=float(colonnes[1].text[:-3])   # pression (hPa)
                temp=float(colonnes[2].text[:-2])    # températre (°c)
                tpw=float(colonnes[3].text[:-2])     # téta prime w (°C) 
                td=float(colonnes[4].text[:-2])      # point de rosée (°c)
                hum=float(colonnes[5].text[:-2])     # humidité relative (%)
                col_vent=colonnes[-1]                # vent
                ff=float(col_vent.text[:-5])/3.6     # vitesse (m/s)
                dd=col_vent.find_all("img")
                path_png=""
                for x in dd:
                    path_png=x.get("src")
                rang_png=path_png.find(".png")
                rang_vent=path_png.find("vent/")
                icone=path_png[rang_vent+5:rang_png]        # la direction du vent est représentée par une icone 
                direc=dic_vent[icone]                       # direction du vent (degrès, rose de 16 valeurs)
                vent=VentHorizontal_DDFF(direc,ff)
                result["niveaux"].append({"alti":alti,"press":press,"temp":temp,"tpw":tpw,"td":td,"hum":hum,"dd":direc,"ff":ff,"u":vent.u,"v":vent.v})
            num_row=num_row+1
        return (result)

res= getProfilVerticalMeteoCiel()
for key in res:
    print (key," : ",res[key])

"""

for niv in res["niveaux"]:
    print (niv)
    
"""