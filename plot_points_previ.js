function plot_points_previ(data,container,titre,transxAxisLabel){
    // Tracé d'un nuage de points reliés par une ligne
    // data : tableau [x:,valeur:] contenant les données à tracer
    // container : nom de la div de la page appelante où va s'afficher le tracé
    // titre : titre du tracé
    // transxAxisLabel : fonction de conversion (x) de l'affichage des labels de l'axe des x
    
    anychart.onDocumentReady(function () {
    	// create a chart
    	  //console.log(data);
      	var chart = anychart.scatter();
        // create a line series and set the data
        chart.line(data);
        chart.crosshair(true);
        // set the text of the y-label
        chart.crosshair().xLabel().format(function (){
            return transxAxisLabel(this.value);
        });
      	chart.labels(true);  // il y aura des labels sur la courbe
      	chart.labels().fontColor("#ff0000");  // labels de la courbe en rouge
      	chart.labels().fontSize(10);   // taille des labels de la courbe
      	chart.labels().format(function(){
      	    return Number.parseFloat(this.value).toFixed(2);  // Les labels de la courbe n'auront que deux décimales
      	});
      	chart.xScale().ticks().interval(3600*3); // interval entre deux labels sur axe des X
      	chart.xAxis().title("Date et heure (UTC)");  // affichage du titre du tracé
      	chart.xAxis().labels(true);
      	chart.xAxis().labels().rotation(-90);
      	chart.xAxis().staggerMode(true);
      	chart.xAxis().staggerLines(1);
      	chart.xAxis().drawFirstLabel(true);
        chart.xAxis().drawLastLabel(true);
      	chart.xAxis().labels().fontSize(10);
      	chart.xAxis().labels().useHtml(true);
      	chart.xAxis().labels().format(function (){  // modification des labels de l'axe des X
          return transxAxisLabel(this.value);
        });
        var vMarker = chart.rangeMarker();
        //var tstest=1513922000;
        //vMarker.from(tstest);
        //vMarker.to(tstest+60*60*12*1000);
        vMarker.from(Date.now()/1000);
        vMarker.to(Date.now()+60*60*12*1000);
        vMarker.axis(chart.xAxis());
        vMarker.fill("#d7fcda");
        vMarker.zIndex(10);
        // enable major grids
        chart.xGrid(true);
        chart.yGrid(true);
        // enable minor grids 
        chart.xMinorGrid(true);
        chart.yMinorGrid(true);
      	// set the chart title
      	chart.title(titre);
      	// set the container id
      	chart.container(container);
      	// initiate drawing the chart
      	chart.draw();
    });
}