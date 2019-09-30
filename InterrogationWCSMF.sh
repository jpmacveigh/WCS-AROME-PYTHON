date
pkill -9 node
tail -10000 resultPrevi > tempo
cat tempo > resultPrevi
rm tempo
resol=$1  # la résolution ("0025" ou "001") est passée en premier paramètre
fichcoverageIDLabels=$2 # le nom du fichier des coverageIDLabel en second
bash ./fabriqueLesCoverageIDLabels.sh $resol $fichcoverageIDLabels
java TraiteLesCoverageIDLabels $resol $fichcoverageIDLabels
date