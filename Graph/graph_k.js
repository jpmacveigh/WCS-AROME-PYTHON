
//-------------------------------------------------------------
//  Nom Document : graph_k
//  Auteur       : @karamel (Kamel A)
//  Objet        : bibliotheque de graphiques   http://www.javascriptfr.com/
//  Création     : 21.12.2016
//-------------------------------------------------------------

//Contrat de licence Creative commons V3.0 de CodeS-SourceS-CommentCaMarche
//Paternité - Pas d'Utilisation Commerciale - Partage des Conditions Initiales à l'Identique 3.0 France

//http://codes-sources.commentcamarche.net/contents/2-informations-de-copyright



//graph_camenbert
//graph_courbe
//graph_barre
//graph_barre_horizontal
//graph_araignee
//graph_pareto



function graph_camenbert(config){
	
	this.cvs=config.canvas;
	this.data=config.data;
	this.couleur_fond=config.couleur_fond;
	this.ombre_centre=config.ombre_centre;
	this.vide_centre=config.vide_centre;
	this.couleur_contour=config.couleur_contour;
	this.epaisseur_contour=config.epaisseur_contour;
	this.police=config.police;
	this.adresse_req=config.adresse_req;
	this.titre=config.titre;
	this.affiche_legende=config.affiche_legende;
	this.position_centre=config.position_x_centre;
	this.legende_cercle=config.legende_cercle;
	this.legende_pourcent=config.legende_pourcent;
	
	if(config.requete==false){
	
		this.data=config.data;
		this.dessine();
	}

	else{
		this.requete();
	}
}

graph_camenbert.prototype={
	
	requete:function(){

		var that=this;
		this.req = new XMLHttpRequest();
		this.req.onreadystatechange = that.retour_req.bind(that);

		this.req.open("GET", that.adresse_req, true);
		this.req.send();
	},

	retour_req:function(){

		if (this.req.readyState == 4 && this.req.status == 200) {

			this.data = JSON.parse(this.req.responseText);

			this.dessine();
		}
	},

	dessine:function(){

		var couleur=['red','#3C8BD9','green','brown','#54656a','purple','orange','#9683EC','#318CE7','#AFA778','#DF6D14','#DD985C','#067790','#DE3163','#E1CE9A','#6C0277','#FDBFB7','#87E990','#A9EAFE','#806D5A','#80D0D0',"#FD3F92","#40826D","#708D23","#DAB30A"];

		var canvas=document.getElementById(this.cvs);
		var ctx=canvas.getContext("2d");
		var dx = canvas.width;
		var dy = canvas.height;

		ctx.strokeStyle=this.couleur_contour;
		ctx.lineWidth = this.epaisseur_contour;
		var rayon=dy/3;

		ctx.font=this.police;

		ctx.fillStyle=this.couleur_fond;
		ctx.rect(0,0,dx,dy);
		ctx.fill();
		ctx.fillStyle="black";

		var total=0;
		for(var i=0; i<this.data.length;i++){
		total+= this.data[i].valeur;
		}

		var unite=(3.14*2)/total;
		var angle_deb=0;
		var angle_fin=0;

		ctx.save();
		ctx.translate(dx/2+this.position_centre, dy / 2 +10);

		for(var i=0; i<this.data.length;i++){

			ctx.fillStyle=couleur[i];

			angle_fin=(unite*this.data[i].valeur).toFixed(3);
			ctx.beginPath();
			ctx.arc(0,0,rayon,0,angle_fin);
			ctx.lineTo(0, 0);
			ctx.closePath();
			ctx.stroke();
			ctx.fill();

			ctx.rotate(angle_fin);
		}

		if(this.ombre_centre){

			ctx.beginPath();
			ctx.arc(0,0,rayon-15,0,Math.PI*2);
			ctx.closePath();
			ctx.fillStyle="rgba(0,0,0,0.2)";
			ctx.fill();
			ctx.closePath();
		}

		if(this.vide_centre>0){
		ctx.beginPath();
		ctx.arc(0,0,this.vide_centre,0,Math.PI*2);
		ctx.closePath();
		ctx.fillStyle=this.couleur_fond;
		ctx.fill();
		ctx.closePath();
		}

		ctx.restore();
		
		var txt_taille=0

		for(var i=0; i<this.data.length;i++){
			
			var taille=ctx.measureText(this.data[i].nom+" : "+this.data[i].valeur).width
			if(taille>txt_taille){
				txt_taille=taille
			}
		}

		for(var i=0; i<this.data.length;i++){

			if(this.affiche_legende){

				ctx.beginPath();
				ctx.fillStyle=couleur[i]
				ctx.rect(dx-35-txt_taille,(20*i)+50,10,10);
				ctx.closePath();
				ctx.fill();
				ctx.fillStyle="black";
				ctx.textAlign="start";
				ctx.fillText(this.data[i].nom+": "+this.data[i].valeur,dx-20-txt_taille,(20*i)+60); 

			}

			var sin=Math.sin(angle_deb+unite*this.data[i].valeur/2)*(rayon+12);
			var cos=Math.cos(angle_deb+unite*this.data[i].valeur/2)*(rayon+12);

			if(this.legende_cercle){

				ctx.textAlign=cos < 0 ? "end" : "start";
				
				var valeur=this.legende_pourcent ? (this.data[i].valeur*(100/total)).toFixed(1)+"%" : this.data[i].valeur;
				
				
				ctx.fillText(this.data[i].nom+":"+valeur,cos+(dx/2+this.position_centre), sin+(dy/2)+10); 
			}

			angle_deb+=(unite*this.data[i].valeur);
		}

		ctx.moveTo(0,0);
		ctx.textAlign="center";
		ctx.font="Italic Bold "+this.police;
		ctx.fillText(this.titre,dx/2,25);
	}
}


/////////////////////
////////////////////

function graph_courbe(config){

	this.cvs=config.canvas;
	this.couleur_fond=config.couleur_fond;
	this.bord=config.bord;
	this.bord_bas=config.bord_bas;
	this.axe_y_max=config.axe_y_max;
	this.axe_y_min=config.axe_y_min;
	this.repere=config.repere;
	this.sous_repere=config.sous_repere;
	this.ligne_repere=config.ligne_repere;
	this.moyenne=config.moyenne;
	this.affiche_valeur=config.affiche_valeur;
	this.police=config.police;
	this.adresse_req=config.adresse_req;
	this.titre=config.titre;
	this.affiche_legende=config.affiche_legende;
	
	this.cvs_detecte=config.cvs_detecte ? new kvs_drag(config.canvas) : false;	
	
	if(config.requete==false){
	
		this.data=config.data;
		this.dessine();
	}

	else{
		this.requete();
	}
}
	
graph_courbe.prototype={

	requete:function(){

		var that=this	;
		this.req = new XMLHttpRequest();
		this.req.onreadystatechange = that.retour_req.bind(that);

		this.req.open("GET", that.adresse_req, true);
		this.req.send();

	},

	retour_req:function(){

		if (this.req.readyState == 4 && this.req.status == 200) {

			this.data = JSON.parse(this.req.responseText);

			this.dessine();
		}
	},
	
	dessine:function(){

		var couleur=['red','#3C8BD9','green','brown','#54656a','purple','orange','#9683EC','#318CE7','#AFA778','#DF6D14','#DD985C','#067790','#DE3163','#E1CE9A','#6C0277','#FDBFB7','#87E990','#A9EAFE','#806D5A','#80D0D0',"#FD3F92","#40826D","#708D23","#DAB30A"];

		var canvas=document.getElementById(this.cvs);
		var ctx=canvas.getContext("2d");
		var dx = canvas.width;
		var dy = canvas.height;

		ctx.font=this.police;

		var taille_g=ctx.measureText(this.axe_y_max).width;

		var largeur=(dx-taille_g-10-this.bord*2);
		var hauteur=dy-(this.bord*2+this.bord_bas)-60;
		var distance=largeur/this.data[0].length;

		var echelle=this.axe_y_min<=0 ? hauteur/(this.axe_y_max+Math.abs(this.axe_y_min)) : hauteur/(this.axe_y_max-this.axe_y_min);

		ctx.fillStyle=this.couleur_fond;
		ctx.rect(0,0,dx,dy);
		ctx.fill();
		ctx.fillStyle="black";

		ctx.strokeStyle="gray";

		ctx.save();
		ctx.translate(taille_g+10+this.bord,(dy-this.bord_bas-this.bord));

		var dixaine=this.repere;
		var multiple=this.axe_y_min;
		var val_sous=this.sous_repere==0 ? 1 : this.sous_repere;

		var qt=this.axe_y_min> 0 ? this.axe_y_max-this.axe_y_min : Math.abs(this.axe_y_min)+this.axe_y_max;

		var distance_x=dx-(this.bord*2)-taille_g-30;
		
		for(var i=0; i<=qt;i+=val_sous){

			if(dixaine==this.repere){
				ctx.beginPath();
				ctx.moveTo(0,-echelle*i);

				if(this.ligne_repere){
					ctx.lineTo(distance_x,-echelle*i);
					ctx.strokeStyle=multiple == 0 ? "black" : "gray";
				}

				ctx.lineTo(- 12,-echelle*i);
				ctx.stroke();
				ctx.closePath();
				ctx.textAlign="end";
				
				ctx.font=multiple == 0 ? "bold "+this.police : this.police;
				
				ctx.fillText(multiple,- 15,-echelle*i);
				dixaine=0;
				multiple+=this.repere;

			}
			else if(this.sous_repere>0){
				ctx.beginPath();
				ctx.moveTo(0,-echelle*i);
				ctx.lineTo(- 8,-echelle*i);
				ctx.stroke();
				ctx.closePath();
			}

			dixaine+=val_sous;
		}
		ctx.restore();
		ctx.strokeStyle="black";
		ctx.save();
		ctx.translate(taille_g+10+this.bord,this.bord+60);

		ctx.beginPath();
		ctx.moveTo(0,0);
		ctx.lineTo(0,hauteur);
		ctx.lineTo(largeur,hauteur);

		ctx.stroke();	
		ctx.restore();

		if(this.moyenne){

			for(var h=1; h<this.data.length;h++){

				this.moyenne=0;

				for(var i=1; i<this.data[h].length;i++){
					this.moyenne+=this.data[h][i].valeur;

				}
				this.moyenne=(this.moyenne/(this.data[h].length-1)).toFixed(2);

				ctx.save()

				ctx.translate(taille_g+10+this.bord,(this.bord+60+echelle*this.axe_y_max)-echelle*this.moyenne)

				ctx.lineWidth = 1;
				ctx.font="11px Verdana";
				ctx.textAlign="end" 
				ctx.strokeStyle=couleur[h-1];
				ctx.fillStyle=couleur[h-1];
				ctx.beginPath();
				ctx.moveTo(0,0);
				ctx.lineTo(largeur,0);
				ctx.closePath();
				ctx.stroke();
				ctx.fillText(this.moyenne,largeur,-10);
				ctx.restore();
			}
		}

		ctx.strokeStyle="black";
		ctx.lineWidth = 2;
		ctx.font=this.police;

		for(var h=1; h<this.data.length;h++){

			ctx.save();

			var dec_x=taille_g+10+this.bord
			var dec_y=this.bord+60+echelle*this.axe_y_max
			
			ctx.translate(taille_g+10+this.bord,this.bord+60+echelle*this.axe_y_max);

			ctx.moveTo(0,0);
			ctx.strokeStyle=couleur[h-1];
			ctx.fillStyle=couleur[h-1];
			ctx.beginPath();

			for(var i=1; i<this.data[h].length;i++){

				ctx.lineTo(0,-this.data[h][i].valeur*echelle);

				if(!this.cvs_detecte){

					ctx.arc(0,-this.data[h][i].valeur*echelle,2,0,Math.PI*2);
				}

				if(this.affiche_valeur){

					ctx.font="11px Verdana";
					ctx.textAlign= i==1 ? "start" : "center";
					ctx.fillText(this.data[h][i].valeur,1,-this.data[h][i].valeur*echelle-12);
				}

				ctx.translate(distance,0);

			}
			ctx.stroke();
			
			ctx.translate(-(distance*(this.data[h].length-1)),0);
			
			if(this.cvs_detecte){
						
				for(var i=1; i<this.data[h].length;i++){

					this.cvs_detecte.n_cercle(0,-this.data[h][i].valeur*echelle,4,couleur[h-1],this.data[0][i-1]+": "+this.data[h][i].valeur,dec_x,dec_y,false);

					ctx.translate(distance,0);
					dec_x+=distance

				}
			}

			ctx.restore();
		}

		ctx.save();
		ctx.translate(taille_g+10+this.bord,dy-this.bord_bas-this.bord+20);

		ctx.moveTo(0,0);

		for(var i=0; i<this.data[0].length;i++){

			ctx.save();
			ctx.rotate(3.14/6);
			ctx.textAlign="start";
			ctx.fillText(this.data[0][i],0,0);
			ctx.restore();
			ctx.translate(distance,0);
		}
		ctx.restore()

		if(this.affiche_legende){
	
			ctx.save();
			ctx.translate(taille_g+10+this.bord,this.bord+35);

			ctx.moveTo(0,0);

			for(var h=1; h<this.data.length;h++){

				var txt=this.data[h][0].nom
				var taille=ctx.measureText(txt).width

				ctx.beginPath();
				ctx.fillStyle=couleur[h-1]
				ctx.rect(0,0,10,10);
				ctx.closePath();
				ctx.fill();
				ctx.stroke();
				ctx.fillStyle="black";
				ctx.textBaseline="middle";
				ctx.textAlign="start";
				ctx.fillText(txt,15,5);

				ctx.translate(taille+25,0);
			}
			ctx.restore();

		}
		ctx.textAlign="center";
		ctx.font="Italic Bold "+this.police;
		ctx.fillText(this.titre,dx/2,this.bord+20);
	}
}

////////////////////////
////////////////////////


function graph_barre(config){

	this.cvs=config.canvas;
	this.data=config.data;
	this.couleur_fond=config.couleur_fond;
	this.espace=config.espace;
	this.bord=config.bord;
	this.bord_bas=config.bord_bas;
	this.axe_y_max=config.axe_y_max;
	this.axe_y_min=config.axe_y_min;
	this.repere=config.repere;
	this.sous_repere=config.sous_repere;
	this.ligne_repere=config.ligne_repere;
	this.moyenne=config.moyenne;
	this.police=config.police;
	this.adresse_req=config.adresse_req;
	this.titre=config.titre;
	this.affiche_valeur=config.affiche_valeur;
	this.affiche_legende=config.affiche_legende;
	this.multicouleur=config.multicouleur;
	
	this.cvs_detecte=config.cvs_detecte ? new kvs_drag(config.canvas) : false;	

	if(config.requete==false){
	
		this.data=config.data
		this.dessine()
	}

	else{
		this.requete()
	}
}

graph_barre.prototype={

	requete:function(){

		var that=this	
		this.req = new XMLHttpRequest();
		this.req.onreadystatechange = that.retour_req.bind(that);

		this.req.open("GET", that.adresse_req, true);
		this.req.send();
	},

	retour_req:function(){

		if (this.req.readyState == 4 && this.req.status == 200) {

			this.data = JSON.parse(this.req.responseText);

			this.dessine();
		}
	},

	dessine:function(){

		var couleur=['#3C8BD9','#2CA02C','brown','#54656a','purple','orange','#9683EC','#318CE7','#AFA778','#DF6D14','#DD985C','#067790','#DE3163','#E1CE9A','#6C0277','#FDBFB7','#87E990','#A9EAFE','#806D5A','#80D0D0',"#FD3F92","#40826D","#708D23","#DAB30A"];

		var canvas=document.getElementById(this.cvs);
		var ctx=canvas.getContext("2d");
		var dx = canvas.width;
		var dy = canvas.height;

		var taille_g=ctx.measureText(this.axe_y_max).width;
		
		var largeur=(dx-taille_g-25-this.bord*2-(this.espace*this.data.length))/this.data.length;
		var hauteur=dy-(this.bord*2+this.bord_bas+60);

		var distance_x=dx-(this.bord*2)-taille_g-30;

		var echelle=this.axe_y_min> 0 ?  hauteur/(this.axe_y_max-this.axe_y_min) : hauteur/(this.axe_y_max+Math.abs(this.axe_y_min));
		
		var qt=this.axe_y_min> 0 ? this.axe_y_max-this.axe_y_min : Math.abs(this.axe_y_min)+this.axe_y_max;

		ctx.fillStyle=this.couleur_fond;
		ctx.rect(0,0,dx,dy);
		ctx.fill();
		ctx.fillStyle="black";

		ctx.strokeStyle="black";

		ctx.save();
		ctx.translate(taille_g+25+this.bord,hauteur+this.bord+60);

		var dixaine=this.repere;
		var multiple=this.axe_y_min;
		var val_sous=this.sous_repere==0 ? 1 : this.sous_repere;
		
		
		for(var i=0; i<=qt;i+=val_sous){

			if(dixaine==this.repere){
				ctx.beginPath();
				ctx.moveTo(0,-echelle*i);

				if(this.ligne_repere){
					ctx.lineTo(distance_x,-echelle*i);
					ctx.strokeStyle=multiple == 0 ? "black" : "gray";
				}

				ctx.lineTo(- 12,-echelle*i);
				ctx.stroke();
				ctx.closePath();
				ctx.textAlign="end";
				
				ctx.font=multiple == 0 ? "bold "+this.police : this.police;
				
				ctx.fillText(multiple,- 15,-echelle*i);
				dixaine=0;
				multiple+=this.repere;

			}
			else if(this.sous_repere>0){
				ctx.beginPath();
				ctx.moveTo(0,-echelle*i);
				ctx.lineTo(- 8,-echelle*i);
				ctx.stroke();
				ctx.closePath();
			}

			dixaine+=val_sous;
		}

		ctx.beginPath();
		ctx.moveTo(0,0);
		ctx.lineTo(0,-echelle*qt);

		ctx.stroke();
		ctx.restore();

		if(this.moyenne){

			var moyenne=0
			var qt=0
			var nbr=0
			
			for(var i=0; i<this.data.length;i++){

				var hauteur_rec=null;
				var nbr=0;

				for (var prop in this.data[i]){

					if(hauteur_rec==null){

						hauteur_rec=0;
					}
					else{
						moyenne+=this.data[i][prop]
						qt++
						nbr++
					}
				}
			}

			moyenne=(moyenne/(qt/nbr)).toFixed(2);
			ctx.save()

			ctx.translate(taille_g+25+this.bord,(this.bord+60+echelle*this.axe_y_max)-echelle*moyenne)

			ctx.lineWidth = 1;
			ctx.font=this.police;
			ctx.strokeStyle="gray"
			ctx.fillStyle="gray"
			ctx.beginPath();
			ctx.moveTo(-5,0);
			ctx.lineTo(distance_x,0);
			ctx.closePath();
			ctx.stroke();
			ctx.fillText(moyenne,-40,0);
			ctx.restore();
		}

		ctx.strokeStyle="black";
		ctx.lineWidth = 2;
		ctx.font=this.police;

		var nbr=0
		
		for (var prop in this.data[0]){
			nbr++
		}
		ctx.save();

		var y_supp=this.axe_y_min> 0 ? echelle*this.axe_y_min : 0;
		
		
		var dec_x=taille_g+25+this.bord;
		var dec_y=this.bord+60+echelle*this.axe_y_max - y_supp;
		
		ctx.translate(taille_g+25+this.bord,this.bord+60+echelle*this.axe_y_max - y_supp);
		
		for(var i=0; i<this.data.length;i++){

			var hauteur_rec=null;
			var coul=0;
			var cpt=0
			
			for (var prop in this.data[i]){
				
				cpt++
				
				if(cpt>1){

					if(hauteur_rec==null){

						hauteur_rec=this.data[i][prop] < 0 ? Math.abs(this.data[i][prop]*echelle) : 0;
					}
					ctx.beginPath();

					if(this.cvs_detecte){
						
						if(this.multicouleur && nbr==2){

							var coul2=couleur[i]
						}
						else{
							var coul2=couleur[coul]
						}

						ctx.fillStyle=coul2;

						this.cvs_detecte.n_rectangle(0,hauteur_rec,largeur,-Math.abs(this.data[i][prop]*echelle)+y_supp,coul2,this.data[i].nom+": "+this.data[i][prop],dec_x,dec_y,false);
					}
					else{
						
						ctx.rect(0,hauteur_rec,largeur,-Math.abs(this.data[i][prop]*echelle)+y_supp);
					}
					
					

					if(nbr==2 && this.affiche_valeur){

						ctx.textAlign="center";
						ctx.fillStyle="black";

						if(this.data[i][prop]>=0){

							ctx.fillText(this.data[i][prop],largeur-largeur/2,-(this.data[i][prop]*echelle)-6+y_supp);
						}
						else{
							ctx.fillText(this.data[i][prop],largeur-largeur/2,-(this.data[i][prop]*echelle)+13);
						}
					}
					
					if(this.multicouleur && nbr==2){

						ctx.fillStyle=couleur[i]
					}
					else{
						ctx.fillStyle=couleur[coul]
					}

					ctx.closePath();
					ctx.fill();
					ctx.stroke();
					coul++;

					hauteur_rec-=Math.abs(this.data[i][prop]*echelle);
				}
			}

			ctx.translate(this.espace+largeur,0);
			dec_x+=this.espace+largeur
			
		}
		ctx.restore();

		ctx.save();
		ctx.translate(taille_g+25+this.bord,this.bord+60+hauteur);

		for(var i=0; i<this.data.length;i++){

			ctx.save();
			ctx.translate(0,10);
			ctx.rotate(3.14/6);
			ctx.textAlign="start";
			ctx.fillText(this.data[i].nom,largeur-largeur/2,-10);
			ctx.restore();

			ctx.translate(this.espace+largeur,0);

		}
		ctx.restore();
		
		
		if(this.affiche_legende){
	
			ctx.save();
			ctx.translate(taille_g+25+20+this.bord,this.bord+35);

			ctx.moveTo(0,0);

				var hauteur_rec=null;
				var coul=0;

				for (var prop in this.data[0]){

					if(hauteur_rec==null){

						hauteur_rec=0;
					}
					else{
				
						var txt=prop;
						var taille=ctx.measureText(txt).width;

						ctx.beginPath();
						ctx.fillStyle=couleur[coul];
						ctx.rect(0,0,10,10);
						ctx.closePath();
						ctx.fill();
						ctx.stroke();
						ctx.fillStyle="black";
						ctx.textBaseline="middle";
						ctx.textAlign="start";
						ctx.fillText(txt,15,5);
						coul++

						ctx.translate(taille+25,0);
					}
				}

			ctx.restore();

		}

		ctx.restore();

		ctx.textAlign="center";
		ctx.font="Italic Bold "+this.police;
		ctx.fillText(this.titre,dx/2,this.bord+15);
	}
}

//////////////////////////////////////
////////////////////////////////////////


function graph_araignee(config){

	this.cvs=config.canvas;
	this.data=config.data;
	this.couleur_fond=config.couleur_fond;
	this.rang=config.rang;
	this.repere=config.repere;
	this.police=config.police;
	this.adresse_req=config.adresse_req;
	this.titre=config.titre;
	this.couleur_graph=config.couleur_graph;
	this.couleur_police=config.couleur_police;
	this.multicolor=config.multicolor;
	this.cvs_detecte=config.cvs_detecte ? new kvs_drag(config.canvas) : false;	
	
	if(config.requete==false){
	
		this.data=config.data
		this.dessine()
	}

	else{
		this.requete()
	}
}

graph_araignee.prototype={

	requete:function(){

		var that=this	
		this.req = new XMLHttpRequest();
		this.req.onreadystatechange = that.retour_req.bind(that);

		this.req.open("GET", that.adresse_req, true);
		this.req.send();

	},

	retour_req:function(){

		if (this.req.readyState == 4 && this.req.status == 200) {

			this.data = JSON.parse(this.req.responseText);

			this.dessine();
		}
	},
	
	dessine:function(){

		var couleur=['red','#3C8BD9','green','brown','#54656a','purple','orange','#9683EC','#AFA778','#DF6D14','#DD985C','#067790','#DE3163','#E1CE9A','#6C0277','#FDBFB7','#87E990','#A9EAFE','#806D5A','#80D0D0',"#FD3F92","#40826D","#708D23","#DAB30A"];

		var canvas=document.getElementById(this.cvs);
		var ctx=canvas.getContext("2d");
		var dx = canvas.width;
		var dy = canvas.height;

		var rayon=dy/3;

		var rayon_cran=rayon/this.rang;

		ctx.fillStyle=this.couleur_fond;
		ctx.rect(0,0,dx,dy);
		ctx.fill();
		ctx.fillStyle="black";

		ctx.strokeStyle="#cccccc";
		ctx.lineWidth = 2;
		ctx.font=this.police;

		var angle_cran=3.14*2/(this.data.length);
		var angle_deb=0;

		for(var h=0; h<this.rang;h++){

			if(h==this.rang-this.repere){

			ctx.strokeStyle="black";

			}
			ctx.beginPath();

			var sin=Math.sin(angle_deb+angle_cran-3.14/2)*rayon;
			var cos=Math.cos(angle_deb+angle_cran-3.14/2)*rayon;

			ctx.moveTo(cos+(dx/2), sin+(dy/2+20));

			for(var i=0; i<this.data.length;i++){

				var sin=Math.sin(angle_deb+angle_cran-3.14/2)*rayon;
				var cos=Math.cos(angle_deb+angle_cran-3.14/2)*rayon;

				ctx.lineTo(cos+(dx/2), sin+(dy/2+20));			

				angle_deb+=angle_cran;
			}
			ctx.closePath();
			ctx.stroke();
			rayon-=rayon_cran;
			ctx.strokeStyle="#cccccc";
		}
		ctx.save();
		ctx.translate(dx/2, dy/2+20);
		
		ctx.rotate(-3.14/2+angle_cran);

		var rayon=dy/3;
		
		for(var i=0; i<this.data.length;i++){
			ctx.beginPath();
			ctx.strokeStyle=this.multicolor ? couleur[i] : this.couleur_police
			ctx.moveTo(0,0);
			ctx.lineTo(rayon,0);
			ctx.stroke();
			ctx.rotate(angle_cran);
		}
		ctx.restore();

		angle_deb=0;
		ctx.beginPath();

		ctx.strokeStyle=this.couleur_graph;
		ctx.lineWidth = 3;

		for(var i=0; i<this.data.length;i++){

			var sin=Math.sin(angle_deb+angle_cran-3.14/2)*rayon_cran*this.data[i].valeur;
			var cos=Math.cos(angle_deb+angle_cran-3.14/2)*rayon_cran*this.data[i].valeur;

			ctx.lineTo(cos+(dx/2), sin+(dy/2+20));
			
			angle_deb+=angle_cran;
		}
		ctx.closePath();
		ctx.stroke();
		
		if(this.cvs_detecte){
		
			angle_deb=0;
			
			for(var i=0; i<this.data.length;i++){

				var sin=Math.sin(angle_deb+angle_cran-3.14/2)*rayon_cran*this.data[i].valeur;
				var cos=Math.cos(angle_deb+angle_cran-3.14/2)*rayon_cran*this.data[i].valeur;

				this.cvs_detecte.n_cercle(cos+(dx/2),sin+(dy/2+20),6,"rgba(0,0,0,0)",this.data[i].nom+": "+this.data[i].valeur,-6,-3,true);
				
				angle_deb+=angle_cran;
			}
		}

		ctx.lineWidth = 2;

		for(var i=0; i<this.data.length;i++){

			ctx.fillStyle=this.multicolor ? couleur[i] : this.couleur_police
			
			var sin=Math.sin(angle_deb+angle_cran-3.14/2)*(rayon+15);
			var cos=Math.cos(angle_deb+angle_cran-3.14/2)*(rayon+15);

			ctx.textAlign=cos < 0 ? "end" : "start";
			ctx.fillText(this.data[i].nom+" : "+this.data[i].valeur,cos+(dx/2), sin+(dy/2+20)); 

			angle_deb+=angle_cran; 
		}
		ctx.textAlign="center";
		ctx.fillStyle="white";
		ctx.font="Italic Bold "+this.police;
		ctx.fillText(this.titre,dx/2,25);
	}
}



//////////////////////////////////////////
/////////////////////////////////////////


function graph_pareto(config){

	this.cvs=config.canvas;
	this.data=config.data;
	this.couleur_fond=config.couleur_fond;
	this.espace=config.espace;
	this.bord=config.bord;
	this.bord_bas=config.bord_bas;
	this.axe_y_max=config.axe_y_max;
	this.ligne_repere=config.ligne_repere;
	this.police=config.police;
	this.adresse_req=config.adresse_req;
	this.titre=config.titre;
	this.pourcentage_courbe=config.pourcentage_courbe;
	this.pourcentage_barre=config.pourcentage_barre;
	this.valeur_barre=config.valeur_barre;
	this.couleur_barre=config.couleur_barre;
	this.cvs_detecte=config.cvs_detecte ? new kvs_drag(config.canvas) : false;
	
	if(config.requete==false){
	
		this.data=config.data;
		this.dessine();
	}

	else{
		this.requete();
	}
}
	
graph_pareto.prototype={
	
	requete:function(){

		var that=this;
		this.req = new XMLHttpRequest();
		this.req.onreadystatechange = that.retour_req.bind(that);
		this.req.open("GET", that.adresse_req, true);
		this.req.send();
	},

	retour_req:function(){

		if (this.req.readyState == 4 && this.req.status == 200) {
		
			this.data = JSON.parse(this.req.responseText);
			this.dessine();
		}
	},
	
	dessine:function(){

		var canvas=document.getElementById(this.cvs);
		var ctx=canvas.getContext("2d");
		var dx = canvas.width;
		var dy = canvas.height;

		ctx.fillStyle=this.couleur_fond;
		ctx.rect(0,0,dx,dy);
		ctx.fill();
		ctx.fillStyle="black";

		ctx.strokeStyle="black";
		
		this.total_valeur=0;
		
		for(var i=0; i<this.data.length;i++){
		this.total_valeur+= this.data[i].valeur;
		}
		
		ctx.font=this.police;
		
		var taille_g=ctx.measureText(this.total_valeur.toFixed(1)).width;

		var taille_d=ctx.measureText("100%").width;
		
		var largeur=dx-taille_g-taille_d-this.bord*2-20;
		var largeur_barre=(largeur-(this.espace*this.data.length))/this.data.length;
		var hauteur=dy-(this.bord*2+this.bord_bas+50);

		var echelle=hauteur/this.total_valeur;
		
		var un_pourcent=this.total_valeur/100;
		
		ctx.save();
		ctx.translate(this.bord+10+taille_g,dy-this.bord_bas-this.bord);

		var multiple=0;

		for(var i=0; i<=hauteur;i+=hauteur/10){

			ctx.beginPath();
			ctx.moveTo(0,-i);

			if(this.ligne_repere){
				ctx.lineTo((largeur_barre+this.espace)*this.data.length,-i);
			}
			ctx.lineTo(- 10,-i);
			ctx.stroke();
			ctx.closePath();
			ctx.textAlign="end";
			
			ctx.fillText((multiple*un_pourcent).toFixed(1),-15,-i);
			
			ctx.textAlign="start";

			ctx.fillText(multiple+"%",largeur+10,-i);

			multiple+=10;
		}

		ctx.restore();

		ctx.save();
		ctx.translate(this.bord+10+taille_g,this.bord_bas+this.bord);

		ctx.beginPath();
		ctx.moveTo(0,0);
		ctx.lineTo(0,hauteur);
		ctx.lineTo(largeur_barre,hauteur);

		ctx.stroke();	
		ctx.restore();

		ctx.strokeStyle="black";
		ctx.lineWidth = 2;
		ctx.font=this.police;

		ctx.save();
		ctx.translate(this.bord+10+taille_g,dy-this.bord_bas-this.bord);

		var dec_x=this.bord+10+taille_g;
		var dec_y=dy-this.bord_bas-this.bord;
		
		for(var i=0; i<this.data.length;i++){

			ctx.beginPath();
			ctx.fillStyle=this.couleur_barre;
			
			if(this.cvs_detecte){
				
				var pct=(this.data[i].valeur/un_pourcent).toFixed(1)+"%";
				this.cvs_detecte.n_rectangle(0,0,largeur_barre,-(this.data[i].valeur*echelle),this.couleur_barre,this.data[i].nom+": "+this.data[i].valeur+" ("+pct+")",dec_x,dec_y,true);
			}
			else{
				ctx.rect(0,0,largeur_barre,-(this.data[i].valeur*echelle));
			}
			
			ctx.closePath();
			ctx.fill();
			ctx.stroke();

			ctx.fillStyle="black";
			ctx.textAlign="center";

			if(this.pourcentage_barre){

				var pct=(this.data[i].valeur/un_pourcent).toFixed(1)+"%";

				ctx.fillText(pct,largeur_barre-largeur_barre/2,-(this.data[i].valeur*echelle)-14);
			}

			if(this.valeur_barre){
				ctx.fillText(this.data[i].valeur,largeur_barre-largeur_barre/2,-(this.data[i].valeur*echelle)+12);
			}

			ctx.translate(this.espace+largeur_barre,0);
			dec_x+=this.espace+largeur_barre;
		}
		ctx.restore();
		
		ctx.save();
		
		ctx.translate(this.bord+10+taille_g,hauteur+this.bord+60);

		for(var i=0; i<this.data.length;i++){

			ctx.save();
			ctx.translate(0,10);
			ctx.rotate(3.14/6);
			ctx.textAlign="start";
			ctx.fillText(this.data[i].nom,0,0);
			ctx.restore();

			ctx.translate(this.espace+largeur_barre,0);

		}
		ctx.restore();

		ctx.save();
		ctx.translate(this.bord+10+taille_g,dy-this.bord_bas-this.bord);

		var plus=0;
		var cran=0;
		var quantite=0;

		ctx.strokeStyle="red";
		ctx.beginPath();

			for(var i=0; i<=this.data.length;i++){

				ctx.lineTo(cran,plus);

					ctx.arc(cran,plus,2,0,Math.PI*2);

				if(i<this.data.length){

					quantite+=this.data[i].valeur;

					var pourcent=(quantite/un_pourcent).toFixed(1)+"%";

					cran+=this.espace+largeur_barre;
					plus-=(this.data[i].valeur*echelle);

					if(this.pourcentage_courbe){

						if(!this.pourcentage_barre){
							ctx.fillText(pourcent,cran-15,plus-15);
						}
						else{
							if( i>0){
								ctx.fillText(pourcent,cran-15,plus-15);
							}
						}
					}
				}
			}
			ctx.stroke();
			
			if(this.cvs_detecte){
	
				plus=0;
				cran=0;
				quantite=0;
				
				for(var i=0; i<this.data.length;i++){

					cran+=this.espace+largeur_barre;
					plus-=(this.data[i].valeur*echelle);
					quantite+=this.data[i].valeur;
					
					var pourcent=(quantite/un_pourcent).toFixed(1);
					
					var contenu=pourcent+"%<br>"+Math.round((100/this.data.length)*(i+1))+"/"+Math.round(pourcent)
					
					this.cvs_detecte.n_cercle(cran,plus,8,"rgba(0,0,0,0.0)",contenu,this.bord+10+taille_g-8,dy-this.bord_bas-this.bord,true);
				}
			}

		ctx.restore();
		ctx.textAlign="center";
		ctx.font="Italic Bold "+this.police;
		ctx.fillText(this.titre,dx/2,this.bord+15);
	}
}


/////////////////////////////
//////////////////////////////



function graph_honrizontal(config){

	this.cvs=config.canvas;
	this.data=config.data;
	this.couleur_fond=config.couleur_fond;
	this.espace=config.espace;
	this.bord=config.bord;
	this.bord_gauche=config.bord_gauche;
	this.axe_y_max=null;
	this.police=config.police;
	this.adresse_req=config.adresse_req;
	this.titre=config.titre;
	this.couleur_barre=config.couleur_barre
	this.cvs_detecte=config.cvs_detecte ? new kvs_drag(config.canvas) : false;
	
	if(config.requete==false){
	
		this.data=config.data
		this.axe_y_max=this.data[this.data.length-1].valeur;
		this.dessine()
	}

	else{
		this.requete()
	}
}
	
graph_honrizontal.prototype={
	
	requete:function(){

		var that=this	
		this.req = new XMLHttpRequest();
		this.req.onreadystatechange = that.retour_req.bind(that);

		this.req.open("GET", that.adresse_req, true);
		this.req.send();
	},

	retour_req:function(){

		if (this.req.readyState == 4 && this.req.status == 200) {
		
			this.data = JSON.parse(this.req.responseText);
			this.axe_y_max=this.data[this.data.length-1].valeur;

			this.dessine();
		}
	},
	
	dessine:function(){

		var canvas=document.getElementById(this.cvs);
		var ctx=canvas.getContext("2d");
		var dx = canvas.width;
		var dy = canvas.height;
		ctx.font=this.police;

		var compteur=0

		for(var i=0; i<this.data.length;i++){

			var taille=ctx.measureText(this.data[i].nom).width
			
			if(taille>compteur){

			compteur=taille
			}
		}

		var largeur=dx-this.bord*2-compteur-10;
		var hauteur=(dy-(this.bord*3)-(this.espace*this.data.length)-15)/this.data.length;

		var echelle=largeur/this.axe_y_max;

		ctx.fillStyle=this.couleur_fond;
		ctx.rect(0,0,dx,dy);
		ctx.fill();
		ctx.fillStyle="black";

		ctx.strokeStyle="black";
		ctx.lineWidth = 2;
		ctx.save();
		ctx.translate(this.bord+10+compteur,dy-15-this.bord);
		
		var dec_x=this.bord+10+compteur;
		var dec_y=dy-15-this.bord-hauteur;

		for(var i=0; i<this.data.length;i++){
			
			ctx.fillStyle=this.couleur_barre,
			ctx.beginPath();
			
			
			if(this.cvs_detecte){
				
				this.cvs_detecte.n_rectangle(0,0,(this.data[i].valeur*echelle),hauteur,this.couleur_barre,this.data[i].nom+": "+this.data[i].valeur,dec_x,dec_y,true);
			}
			
			else{
				ctx.rect(0,0,(this.data[i].valeur*echelle),hauteur);
			}
			

			ctx.closePath();
			ctx.fill();
			ctx.stroke()
			ctx.textBaseline="middle";
			ctx.fillStyle="white";
			ctx.textAlign="end";
			ctx.fillText(this.data[i].valeur,this.data[i].valeur*echelle-3,hauteur/2);

			ctx.translate(0,-(this.espace+hauteur));

			dec_y-=(this.espace+hauteur)
		}
		ctx.restore();

		ctx.save();
		ctx.moveTo(0,0)
		ctx.translate(this.bord+compteur,dy-this.bord-15);
		ctx.textAlign="end";
		ctx.font=this.police;
		ctx.textBaseline="middle";
		
		for(var i=0; i<this.data.length;i++){

			ctx.fillText(this.data[i].nom,0,hauteur/2);

			ctx.translate(0,-hauteur-this.espace);

		}
		ctx.restore();

		ctx.textAlign="center";
		ctx.font="Italic Bold "+this.police;
		ctx.fillText(this.titre,dx/2,this.bord+10);
	}
}


/////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////info bull///////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////


function kvs_drag(cvs){

	this.decx=null;
	this.decy=null;
	this.rar=true;
	
	this.obj_json=[];
	this.cvs=document.getElementById(cvs);

	this.couleur='';
	
	this.elem_courant="";
	
	this.bull=document.createElement("div")
	this.bull.style.position="absolute"
	this.bull.style.padding="5px"
	this.bull.style.background="white"
	this.bull.style.border="solid 1px"
	this.bull.style.zIndex="100"
	this.bull.style.display="none"
	document.body.appendChild(this.bull)

	
	this.init();
}

kvs_drag.prototype.new_cercle=function(gc,h,rayon,coul,valeur,tranparence){

	this.type='cercle';
	this.gauche=gc;
	this.haut=h-rayon;
	this.hauteur=rayon*2;
	this.largeur=rayon*2;
	this.couleur=coul;
	this.rayon=rayon;
	this.valeur=valeur;
	this.tranparence=tranparence;
}

kvs_drag.prototype.new_rectangle=function(gc,h,lg,ht,coul,valeur,tranparence){

	this.type='rectangle';
	this.gauche=gc;
	this.haut=h;
	this.largeur=lg;
	this.hauteur=ht
	this.couleur=coul;
	this.valeur=valeur;
	this.tranparence=tranparence;
}

kvs_drag.prototype.new_texte=function(gc,h,ht,lg,coul,popo,txt){

	this.type='texte';
	this.texte=txt;
	this.police=popo;
	this.gauche=gc;
	this.haut=h;
	this.hauteur=ht
	this.largeur=lg;
	this.couleur=coul;
}


kvs_drag.prototype.colision=function(elem){		//interception de la position des elements
	
	if(this.decy >= elem.haut + elem.hauteur		// trop en bas
			|| this.decy <= elem.haut						// trop en haut
			|| this.decx>=elem.gauche + elem.largeur	// trop à droite
			|| this.decx<=elem.gauche){					// trop à gauche
		
		return false;	
	}
	else{
		
		return true;
	}
}


kvs_drag.prototype.init=function(){		//lecture du fichier json et configuration des variables et array
	
	this.cvs.addEventListener("mousemove",this.style_curseur.bind(this), false);
	
	for(var i=0;i<=this.obj_json.length-1;i++){
	
	this.cvs_dessin(i);
	
	}
}



kvs_drag.prototype.style_curseur=function(e){		//gestion du curseur
	
	var bounding=e.currentTarget.getBoundingClientRect()

	if(window.scrollX!=undefined){
		
		this.decx = e.pageX - (bounding.left+scrollX);
		this.decy = e.pageY - (bounding.top+scrollY);
	}
	else{
		
		this.decx = e.pageX - (bounding.left+document.documentElement.scrollLeft);
		this.decy = e.pageY - (bounding.top+document.documentElement.scrollTop);
	}

	this.bull.style.top=e.pageY+10+"px"
	this.bull.style.left=e.pageX+10+'px'
	
	if(this.elem_courant==""){

		for(var i=0;i<this.obj_json.length;i++){

			var elem=this.obj_json[i]

			if(this.colision(elem)){

				this.elem_courant=this.obj_json[i]

				this.cvs.style.cursor='pointer';

				var ctx = this.cvs.getContext("2d");
				ctx.globalAlpha =0.2;
				
				this.couleur=elem.couleur
				
				elem.couleur="black";
				
				this.bull.style.display="block"
				this.bull.innerHTML=elem.valeur

				!elem.tranparence ? this.cvs_dessin() : null;

				break;
			}
		}
	}

	else if(this.elem_courant!=""){

		if(!this.colision(this.elem_courant)){

			this.cvs.style.cursor='default';
			var ctx = this.cvs.getContext("2d");
			ctx.globalAlpha =1;
			this.elem_courant.couleur=this.couleur;
			
			!this.elem_courant.tranparence ? this.cvs_dessin() : null;
			
			this.elem_courant=""
			this.bull.style.display="none"
		}
	}
}

kvs_drag.prototype.cvs_dessin=function(){		// dessin du canvas

	var cvs=this.cvs;
	var ctx = cvs.getContext("2d");
	
	var element=this.elem_courant;
	ctx.fillStyle=element.couleur;

		switch (element.type) {
			
		case "rectangle":
			this.rectangle(ctx,element)
			break;
			
		case "cercle":
			this.cercle(ctx,element)
			break;
			
		case "texte":
			this.texte(ctx,element)
			break;
		}
}


kvs_drag.prototype.rectangle=function(ctx,element){

	ctx.beginPath();
	ctx.rect(element.gauche,element.haut,element.largeur,element.hauteur);
	ctx.closePath()
	ctx.fill();
	ctx.stroke();
}
		
kvs_drag.prototype.cercle=function(ctx,element){
	ctx.beginPath();
	ctx.arc(element.gauche,element.haut+element.rayon, element.rayon, 0, Math.PI*2);
	ctx.closePath()
	ctx.fill();
}


kvs_drag.prototype.texte=function(ctx,element){
		
	ctx.fillStyle=element.couleur;
	ctx.font = element.police;
	ctx.fillText(element.texte, element.gauche, (element.haut+element.hauteur));
}



kvs_drag.prototype.n_cercle=function(gc,h,rayon,coul,valeur,dec_x,dec_y,tranparence){
	
	this.obj_json.push(new this.new_cercle(gc,h,rayon,coul,valeur,tranparence))

	var element=this.obj_json[this.obj_json.length-1]

	var ctx = this.cvs.getContext("2d");
	ctx.fillStyle=element.couleur;

	this.cercle(ctx,element)
	
	element.gauche+=dec_x;
	element.haut+=dec_y;
	
}

kvs_drag.prototype.n_rectangle=function(gc,h,lg,ht,coul,valeur,dec_x,dec_y,tranparence){
	
	this.obj_json.push(new this.new_rectangle(gc,h,lg,ht,coul,valeur,tranparence))

	var element=this.obj_json[this.obj_json.length-1]

	var ctx = this.cvs.getContext("2d");
	ctx.fillStyle=element.couleur;
		
	this.rectangle(ctx,element)
	
	element.gauche+=dec_x;
	element.haut+=(dec_y+ht);

	element.hauteur=Math.abs(element.hauteur)
	element.largeur=Math.abs(element.largeur)
	
}


kvs_drag.prototype.n_texte=function(gc,h,ht,lg,coul,popo,txt){
	
	this.obj_json.push(new this.new_texte(gc,h,ht,lg,coul,popo,txt))

	var element=this.obj_json[this.obj_json.length-1]

	var ctx = this.cvs.getContext("2d");
	ctx.fillStyle=element.couleur;
	ctx.font = element.police;
	element.largeur= ctx.measureText(element.texte).width;
	
	this.texte(ctx,element)
	
}