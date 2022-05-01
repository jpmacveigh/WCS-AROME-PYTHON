import datetime
def dateLimiteRetention(ecart_heure):  # calcul la date limite de rétention à partir d'un écart (secondes) à maintenant dans la passé
        # format requis : 2019-08-01T09:46:18Z
        format="%Y-%m-%dT%XZ"  # pour avoir le format requis
        now=datetime.datetime.utcnow()  # date actuelle UTC
        ret=now-datetime.timedelta(seconds=ecart_heure*3600.) # on retranche l'écart en secondes à la date actuelle
        ret=ret.strftime(format)  # formatage de la réponse
        #print (now.strftime(format))
        return ret
#print (dateLimiteRetention(48))  # pour un écart de 5 heures en arrière