import math
def distanceOrthodromique (rlonb,rlatb,rlonc,rlatc):
    '''
        c  J.P. Mac Veigh le 27/2/88
        c  Calcul de la distance (m) orthodromique entre deux points B et C de la surface
        c  de la terre définis par leur latitude et longitude.
        c  On résoud le triangle sphérique formé par les deux points et le pôle
        c  nord et dont on connait deux côtés (les compléments des latitudes
        c  des deux points) et l'angle compris (la différence des longitudes des
        c  deux points).
        c  Référence: Cours d'Astronomie
        c             H. Andoyer
        c             première partie, troisième édition, page 24
        c             Librairie Scientifique J. Hermann, 1923.
        */'''
    if rlonb==rlonc and rlatb==rlatc : return 0.
    r=6366.2031  # rayon de la terre en km
    pi=math.pi
    a=(rlonc-rlonb)*(pi/180)
    rc=(pi/2)-(rlatb*pi/180)
    rb=(pi/2)-(rlatc*pi/180)
    x=math.cos(rb)*math.cos(rc)+math.sin(rb)*math.sin(rc)*math.cos(a)
    if x>1. : x=1.
    elif x<-1.: x=-1.
    ra=math.acos(x)
    d=ra*r
    return 1000.*abs(d)  # retour en mètres
#print (distanceOrthodromique(0.,0.,1.,0.))