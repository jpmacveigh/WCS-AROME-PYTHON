#!/usr/bin/python
# coding: utf8
import datetime
def dateLimiteRetention(ecart):  # calcul la date limite de rétention à partir d'un écart (secondes) à maintenant dans la passé
        # format requis : 2019-08-01T09:46:18Z
        format="%Y-%m-%dT%XZ"  # pour avoir le format requis
        now=datetime.datetime.now()  # date actuelle UTC
        ret=now-datetime.timedelta(seconds=ecart) # on retranche l'écart en secondes à la date actuelle
        ret=ret.strftime(format)  # formatage de la réponse
        print (now.strftime(format))
        return ret
print (dateLimiteRetention(5*60*60*24))  # pour un écart de 5 jours en arrière