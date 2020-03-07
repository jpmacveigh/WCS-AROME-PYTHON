from distanceOrthodromique import distanceOrthodromique
import math
def capVitesse (lona,lata,lonb,latb,deltat):
    ''' Renvoit le cap ]0.,360.] et la vitesse (Km/h) suivi pour se rendre du point a au point b en deltat (secondes) '''
    if deltat == 0. : return (None,None)
    distance = distanceOrthodromique (lona,lata,lonb,latb) #  distance entre a et b (mètres)
    if distance == 0.: return (0.,0.)
    dlong = distanceOrthodromique (lona,lata,lonb,lata)   #  distance en longitude (mètres)
    if dlong>distance : dlong=distance
    alpha = math.asin(dlong/distance)
    alpha = alpha*2./math.pi*90.
    if latb>=lata:
        if lonb<=lona:
            alpha = 360.-alpha
    else :
        if lonb>lona:
            alpha=180.-alpha
        else :
            alpha=180.+alpha
    vitesse = distance/1000./deltat*3600.   # vitesse en Km/h
    return (alpha,vitesse)   # cap suivi en degrès (Nord=360, Est=90, Sud=180, Ouest=270)


print (capVitesse (0.,0.,0.,1.,3600.))
print (capVitesse (0.,0.,1.,1.,3600.))
print (capVitesse (0.,0.,1.,0.,3600.))
print (capVitesse (0.,0.,1.,-1.,3600.))
print (capVitesse (0.,0.,0.,-1.,3600.))
print (capVitesse (0.,0.,-1.,-1.,3600.))
print (capVitesse (0.,0.,-1.,0.,3600.))
print (capVitesse (0.,0.,-1.,1.,3600.))