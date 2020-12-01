import requests
import bs4 as BeautifulSoup
import numpy as np
from VentHorizontal_DDFF import VentHorizontal_DDFF
import json
import datetime
def getProfilVerticalMeteociel (echeance,lati,longi,alti_interpolees=[]):
        ''' Extraction du profil vertical atmosphérique issu du modèle global GFS pour une grille à 0.25°
            et contenu dans une page HTML fournie par Météociel.
            voir : http://www.meteociel.fr/modeles/sondage_gfs.php
            Ce programme a toutes les chances de se planter ou de fournir des données érronnées 
            si la structure de la page HTML est modifiée par Météociel. Quelques contôles sont fait sur les données.
            Les niveaux fournis sont des niveaux pression compris entre 1000 hPa et 175 hPa,
            ainsi que ceux d'une liste indiquéee à l'appel sur lesquels les variables sont interpolées.
            Les variables fournies sont Z(m),P(hPa),T(°C),Tpw(°C),Td(°C),H(%),dd(degrès) et ff(m/s) '''
        assert echeance>=0 , echeance
        if echeance%3 != 0:
            echeance = echeance-echeance%3  # on arrondi l'écheance aux 3 heures entières précédantes
        result={}  #  le resultat sera un dictionnaire Python
        # url pour modèle GFS 0.25° à Lille :
        # http://www.meteociel.fr/modeles/sondage2.php?archive=0&ech=36&map=2&runpara=0&x1=3.07585&lat=50.6288&lon=3.07585&userlat=1&y1=50.6288"
        # alternatif qui marche aussi :
        # http://www.meteociel.fr/modeles/sondage2.php?archive=0&ech=132&map=2&runpara=0&lat=50.6288&lon=3.07585
        url="http://www.meteociel.fr/modeles/sondage2.php?archive=0&ech="+str(echeance)
        url=url+"&map=2&runpara=0"
        url=url+"&lat="+str(lati)+"8&lon="+str(longi)
        result["url"]=url
        print(url)
        codes_vent=["nne","ne","ene","e","ese","se","sse","s","sso","so","oso","o","ono","no","nno","n"]  # on décodera le nom du fichier png de l'icone du vent
        dic_vent={}
        i=1
        for code in codes_vent:     # construction du dictionnaire associant le code vent à une direction en degrés 
            dic_vent[code]=i*22.5   # rose de 16 valeurs pour 360 degrès
            i=i+1
        status=0
        while status != 200:
            r=requests.get(url)      # acquisition de la page HTML
            status=r.status_code
            #print (status)
        res=r.content
        soup=BeautifulSoup.BeautifulSoup(res,"lxml")  # parsing de la page HTML
        tables=[]
        for p in soup.find_all('table'):  #  on extrait toutes les balises <tables> de la page HTML
            tables.append(p)
        
        num_row=0
        for row in tables[0].find_all('tr'):   # la premiere table est celle des données générales du profil
            colonnes=row.find_all('td')        # on extraittoutesles balises <td> de la balise <tr>
            if num_row==0:
                 for colonne in colonnes:
                    col_run=colonne.text       # la définition du run du modèle
                    print(col_run)
                    result["col_run"]=col_run     
                    split=col_run.split()
                    result["an_run"]=int(split[-1])
                    result["mois_run"]=split[-2]
                    mois=["janvier","fevrier","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","decembre"]
                    result["num_mois_run"]=mois.index(result["mois_run"])+1
                    assert 1<=result["num_mois_run"]<=12 , result["num_mois_run"]
                    result["jour_run"]=int(split[-3])
                    result["heure_run"]=int(split[2][:-1])
                    UTC_run=datetime.datetime(result["an_run"],result["num_mois_run"],result["jour_run"],result["heure_run"],tzinfo=datetime.timezone.utc)
                    result["ts_run"]=int(datetime.datetime.timestamp(UTC_run))
                    result["UTC_run_string"]=UTC_run.isoformat()
            else :
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
                        UTC_previ=UTC_run+datetime.timedelta(hours=result["echeance"])
                        result["ts_previ"]=int(datetime.datetime.timestamp(UTC_previ))
                        result["UTC_previ_string"]=UTC_previ.isoformat()
                    num_col=num_col+1
            num_row=num_row+1
        result["altitudes"]=[]   # liste de tous les niveaux présents dans le profil verrticaal
        num_row=0
        alti_min=10000.
        alti_max=-500.
        for row in tables[1].find_all('tr'):# la seconde table de la page est celle des valeurs numérique du profil vertical
            if num_row > 0:                          # on saute la première ligne de la table
                colonnes=row.find_all('td')          # on récupère les colonnes de chaque ligne de la table
                alti=float(colonnes[0].text[:-2])    # la première colonne donne l'altitude (m)
                if (alti<=alti_min): alti_min=alti
                if (alti>=alti_max): alti_max=alti
                press=float(colonnes[1].text[:-3])   # pression (hPa)
                assert 100.<=press<=1000.,press
                temp=float(colonnes[2].text[:-2])    # températre (°c)
                assert -80.<=temp<=60.,temp
                tpw=float(colonnes[3].text[:-2])     # téta prime w (°C) 
                td=float(colonnes[4].text[:-2])      # point de rosée (°c)
                hum=float(colonnes[5].text[:-2])     # humidité relative (%)
                assert 0.<=hum<=100.,hum
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
                result["altitudes"].append({"alti":alti,"press":press,"temp":temp,"tpw":tpw,"td":td,"hum":hum,"dd":direc,"ff":ff,"u":vent.u,"v":vent.v})
            num_row=num_row+1
        result["altitudes"]=sorted(result["altitudes"],key=lambda k:k["alti"]) # on trie, en vue de l'interpolation, les niveaux extraits par altitude croissante
        result["alti_min"]=alti_min
        result["alti_max"]=alti_max
        result["altitudes_interpolees"]=[]     # calcul des valeurs interpolées aux altitudes demandees
        lesAltitudes_interpolees=[x for x in alti_interpolees if (result["alti_min"]<=x) and (x<=result["alti_max"])] #  on se limite aux altitudes entre ali_min et alti_max
        #print(lesAltitudes_interpolees)
        for alti in lesAltitudes_interpolees:
            result["altitudes_interpolees"].append({"alti":alti})
        lesAltitudes=[x for x in [result["altitudes"][i]["alti"] for i in range(len(result["altitudes"]))]]
        #print(lesAltitudes)
        for key in [key for key in result["altitudes"][0].keys() if not key=="alti"]:
            fp=[x for x in [result["altitudes"][i][key] for i in range(len(result["altitudes"]))]]
            #print(key,fp)
            res=np.interp(lesAltitudes_interpolees,lesAltitudes,fp)  # interpolation sur les altitudes damandées
            #print (key,res)
            num_alti_interpolees=0
            for alti in lesAltitudes_interpolees:
                result["altitudes_interpolees"][num_alti_interpolees][key]=res[num_alti_interpolees]
                num_alti_interpolees=num_alti_interpolees+1
            result["altitudes_interpolees"]=sorted(result["altitudes_interpolees"],key=lambda k:k["alti"]) # tri sur les altitudes croissantes
        return (result)

    
res= getProfilVerticalMeteociel(9,50.6,3.06,[10,12,-400,125,528,352,965,8952,12000,15963])
print(json.dumps(res, indent=4, sort_keys=True))


for key in res:
    if not key in ["altitudes","altitudes_interpolees"]:
        print (key," : ",res[key])
print("***************** altitudes du profil vertical **************************************")
for niv in res["altitudes"]:
    print (niv)
print("***************** altitudes interpolees **************************************")
for niv in res["altitudes_interpolees"]:
    print (niv)

