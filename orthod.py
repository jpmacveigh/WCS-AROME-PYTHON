#coding: utf8
import math
def orthod (rlonb,rlatb,rlonc,rlatc):
    """
    c
    c  J.P. Mac Veigh le 27/2/1988
    c  Calcul de la distance orthodromique en km entre deux points B et C de la surface
    c  de la sphère terrestre définis par leur latitude et longitude.
    c  On résoud le triangle sphérique formé par les deux points et le pôle
    c  nord et dont on connait deux côtés (les compléments des latitudes
    c  des deux points) et l'angle compris (la différence des longitudes des
    c  deux points).
    c  Référence: Cours d'Astronomie
    c             H. Andoyer
    c             première partie, troisième ‚édition, page 24
    c             Librairie Scientifique J. Hermann, 1923.
    c  
    """
    r=6370.  # rayon de la terre en km
    pi=math.pi
    a=(rlonc-rlonb)*(pi/180.);
    rc=(pi/2)-(rlatb*pi/180.);
    rb=(pi/2)-(rlatc*pi/180.);
    x=math.cos(rb)*math.cos(rc)+math.sin(rb)*math.sin(rc)*math.cos(a);
    ra=math.acos(x);
    d=ra*r;
    return (abs(d));