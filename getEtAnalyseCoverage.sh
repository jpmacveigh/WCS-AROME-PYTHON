#!/bin/bash
path=$1  # les path à utiliser pour le getCoverage est passé en premier parametre
nomDeLaVariable=$2 # le nom de la variable du modèle
echo "path pour getCoverage : "$path
echo "nom de la variable : "$nomDeLaVariable
curl $path > tifftempo # envoi de la requête getCoverage au service WCS
node ./test_geotiff.js $nomDeLaVariable > resultNode 2>resultNode # décodage et traitement du coverage reçu avec geotiff.js sous node 
       