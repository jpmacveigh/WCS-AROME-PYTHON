<?php
function dessine_serie($db,$rows,$i){
      $qstr ='select nom,now,run,date,val from prevision where nom="'.$rows[$i]["nom"].'" and niv="'.$rows[$i]["niv"].'" order by date';
      echo $qstr; 
      $series=$db->selectArray($qstr);  // extraction de la série temporelle
      AfficheTableauAssociatif('Serie temporelle de : '.$rows[$i]["nom"].' '.$rows[$i]["niv"],$series);
      echo '<div id="courbe'.$i.'" class="trace_courbe">';  // emplacement où l'on va tracer 
      echo 'ici sera la courbe N°: '.$i.'</div>';
      echo '<script> 
        var x='.$i.';
        console.log("x: ",x);</script>';
      echo '<script>
        var data=[';
      for ($j=0;$j<sizeof($series);$j++){
        //echo'{x:'.$j.',value:'.$series[$j]["val"].'},';
        echo'{x:'.chaineDateAromeToTimestamp($series[$j]["date"]).',value:'.$series[$j]["val"].'},';
      }
      echo ']</script>';
      echo '<script>
        var transformxAxisLabel= function (ts){
          return new Date(ts*1000).toISOString();
        };
        plot_points_previ(data,"courbe'.$i.'","'.$rows[$i]["nom"].' '.$rows[$i]["niv"].'",transformxAxisLabel);
      </script><br>';
}
?>
