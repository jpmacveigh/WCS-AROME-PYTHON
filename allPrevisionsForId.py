def allPrevisionsForId (Id,longi,lati,all=True): 
    '''
    Retourne toutes les prévisions au point (longi,lati) contenues dans un objet CoverageId Id
    Si future_only==True, ne retourne que les prévsions qui sont futures par rapport à l'heure actuelle
    '''
    result=[]
    Id.describeCoverage()  # On complète la description de l'Id
    Id.affiche()
    if Id.dim==3 : nbIterationsNiv = 1            
    if Id.dim==4 : nbIterationsNiv = len(Id.__dict__[Id.niv])
    if all == True:
      liste_des_dates=Id.timeDatePrevi
    else :
      liste_des_dates=Id.timeDatePreviFutures
    for numNiv in range(0, nbIterationsNiv) :  # boucle sur les niveaux disponibles dans l'Id
        for date in liste_des_dates :  # boucle sur toutes les dates choisies
            res={}  # dictionnaire résultat pour une prévision
            res["abrev"]=Id.code
            res["run"]=Id.timeUTCRun
            res["unit"]=Id.unite
            res["nom"]=Id.chaineNom()
            res["now"]=chaineUTCFromTs(tsNow())  # heure actuelle à laquelle on extrait la prévision des bases de MF
            if Id.dim==4 : niveau=Id.__dict__[Id.niv][numNiv] # Cas où il faut le niveau.
            if Id.dim==3 : niveau=None  # Cas où le niveau n'est pas requis
            res["z"]=niveau  # position sur la verticale (ou None si dim=3)
            res["niv"]=Id.niv # nom de la coordonnée verticale (ou None si dim=3)
             # on prend la première date des prévisions
            res["date"]=date
            Id.getCoverage(lati-.1,lati+.1,longi-.1,longi+.1,date,niveau)
            res["val"]= Id.valeur(longi,lati)
            print (res["abrev"],res["run"],res["date"],res["z"],res["niv"],res["val"])
            result.append(res) # renvoi une liste de prévisiosn transformée en json 
    return result