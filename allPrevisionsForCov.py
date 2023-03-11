from Utils import chaineUTCFromTs,tsNow
import json
import pyairtable
import os
from traiteAromePrevi import traiteAromePrevi
def allPrevisionsForCov (cov,longi,lati,all_previ=True,grib=False): 
    '''
    Retourne toutes les prévisions au point (longi,lati) contenues dans un objet Coverage cov
    Si all_previ=True  : retourne toutes les prévisions disponible dans le cov
    Si all_previ=False : ne retourne que les prévsions qui sont futures par rapport à l'heure actuelle
    Utilise le format grib ou tiff du coverage selon la valeur du paraètre "grib" 
    '''
    # Accès à la base Météo de Airtable
    from pyairtable import Table
    PAT="patPdSrU8sJ8AERNd.b52225dcf7dd617bca5c544559ce3854199faa45907b6354f44ab7e578b7be71" # Personal Acces Token pour cette base
    baseId="app6VCTcvfW1V6FHh" # Id de la base
    table = Table(PAT,baseId,"Prévisions WCS décodées")  # ouverture de la table de la base Airtable
    result=[]
    cov.describeCoverage()  # On complète la description de l'objet cov
    cov.affiche()
    if cov.dim==3 : nbIterationsNiv = 1            
    if cov.dim==4 : nbIterationsNiv = len(cov.__dict__[cov.niv])
    if all_previ == True:
      liste_des_dates=cov.timeDatePrevi
    else :
      liste_des_dates=cov.timeDatePreviFutures
    for numNiv in range(0, nbIterationsNiv) :  # boucle sur les niveaux disponibles dans l'cov
        for date in liste_des_dates :  # boucle sur toutes les dates choisies
            res={}  # dictionnaire résultat pour une prévision
            res["abrev"]=cov.code
            res["run"]=cov.timeUTCRun
            res["unit"]=cov.unite
            res["nom"]=cov.chaineNom()
            res["now"]=chaineUTCFromTs(tsNow())  # heure actuelle à laquelle on extrait la prévision des bases de MF
            if cov.dim==4 : niveau=cov.__dict__[cov.niv][numNiv] # Cas où il faut le niveau.
            if cov.dim==3 : niveau=None  # Cas où le niveau n'est pas requis
            res["z"]=niveau  # position sur la verticale (ou None si dim=3)
            res["niv"]=cov.niv # nom de la coordonnée verticale (ou None si dim=3)
            res["date"]=date  # on prend la première date des prévisions
            if grib==True:
                cov.getCoverage_grib(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau) # Appel à getCoverage_grib
                res["val"]= cov.nearest_value_grib(longi,lati)["value"]
            else:
                cov.getCoverage_tiff(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau) # Appel à getCoverage_tiff
                res["val"]= cov.nearest_value_tiff(longi,lati)
            print (res["abrev"],res["run"],res["date"],res["z"],res["niv"],res["val"])
            result.append(json.dumps(res)) # renvoi une liste de prévisiosn transformée en json 
            with open("res_tempo.txt","a") as f: # Ecriture dans le fichier res_tempo.txt
                f.write(json.dumps(res)+"\n")
            # Ecriture dans la base Airtable
            if cov.dim == 4:
                record={
                    'Param':res["abrev"],
                    'Niveau':float(res["z"]),
                    'Lati':float(lati),
                    'Longi':float(longi),
                    'Valeur':float(res["val"]),
                    'Date UTC run':res["run"],
                    'Date UTC prévi':res["date"]   
                 }
            else :
                 record={
                    'Param':res["abrev"],
                    'Niveau':0.,
                    'Lati':float(lati),
                    'Longi':float(longi),
                    'Valeur':float(res["val"]),
                    'Date UTC run':res["run"],
                    'Date UTC prévi':res["date"]   
                 }
            print(record)
            # Création pour chaque prévision d'un record dans la table Prévision WCS décodées de la base Météo de Airtable
            table.create(record)
    if len(result) != 0 :
        repcourant=os.getcwd()+"/"
        fic = open(repcourant+"previArome.txt","w") # Ecriture des résultats dans fichier temporaire
        for previ in result:
            fic.writelines(str(previ)+"\n")
        fic.close()
        traiteAromePrevi() # Ecriture du fichier previArome.txt dans base Arome.sqlite
    return result