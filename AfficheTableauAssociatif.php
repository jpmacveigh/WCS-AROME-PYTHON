<?php
    function AfficheTableauAssociatif ($titre,$tab){
        echo '<div class="container">';
        echo '<h2>'.$titre.'</h2>
            <table id="liste_des_valeurs" class="table table-condensed collapse">
              <thead>
                <tr>';
                 foreach ($tab[0] as $cle => $valeur){  // ecriture des entêtes des colonnes
                  echo "<th>".$cle."</th>";
                 }
                echo"</tr>";
              echo'</thead>';
              echo '<tbody id="corps_tableau">';
              for ($i=0; $i<sizeof($tab);$i++){ 
                echo "<tr>";
                foreach ($tab[$i] as $cle => $valeur){  // écriture du contenu de chaque colonne
                    echo '<td>'.$valeur.'</td>';
                }
                echo "</tr>";
              }
              echo '</tbody>
            </table>
          </div>';
          flush();
    }
?>