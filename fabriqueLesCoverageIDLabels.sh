#!/bin/bash
# Traitement avec bash du Web Coverage Service (WCS) de MF
# On exécute successivement :
#   - getCapabilities pour connaitre tous les coveragesID proposés
#   
#
date  # affichage de la date du début des traitements
resol=$1         # le premier paramètre d'appel du script est la résolution du modèle Arome : 001 ou 0025
fichresultat=$2  # le second est le nom du fichier où seront écrit leverageIDLabel
path="https://geoservices.meteofrance.fr/services/MF-NWP-HIGHRES-AROME-"
path=$path$resol"-FRANCE-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"
#curl "https://geoservices.meteofrance.fr/services/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__" > resultGetCapabilities
echo $path  # path pour la requete getCapabilities au service WCS
curl $path > resultGetCapabilities   # requête getCapabilities au service WCS
grep "<wcs:CoverageId>" resultGetCapabilities > toto   
sed  "s/<wcs:CoverageId>/""/g" toto > tata
sed  "s/<\/wcs:CoverageId>/""/g" tata > titi
sed  "s/^[ \t]*//g" titi > $fichresultat   # la liste des coverageID a été fabriquée
rm toto tata titi
date  # affichage de la fin des traitements




