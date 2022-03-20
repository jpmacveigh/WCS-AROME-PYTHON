from Utils import chaineUTCFromTs,tsNow
import json
def allPrevisionsForCov (cov,longi,lati,all_previ=True,grib=False): 
    '''
    Retourne toutes les prévisions au point (longi,lati) contenues dans un objet Coverage cov
    Si all_previ=True  : retourne toutes les prévisions disponible dans le cov
    Si all_previ=False : ne retourne que les prévsions qui sont futures par rapport à l'heure actuelle
    Utilise le format grib ou tiff du coverage selon la valeur du paraètre "grib" 
    '''
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
             # on prend la première date des prévisions
            res["date"]=date
            if grib==True:
                cov.getCoverage_grib(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau)
                res["val"]= cov.nearest_value_grib(longi,lati)["value"]
                cov.getCoverage_tiff(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau)
                print ("vérification tiff==grib")
                assert res["val"]==cov.nearest_value_tiff(longi,lati)  # on vérifie que tiff et grib donne la même valeur
            else:
                cov.getCoverage_tiff(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau)
                res["val"]= cov.nearest_value_tiff(longi,lati)
            print (res["abrev"],res["run"],res["date"],res["z"],res["niv"],res["val"])
            result.append(json.dumps(res)) # renvoi une liste de prévisiosn transformée en json 
    return result