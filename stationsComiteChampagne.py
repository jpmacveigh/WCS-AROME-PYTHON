#coding: utf8
from getWCSCapabilities import previsions
import json

stationsComiteChampagne =[
{	"commune":"Avize","lieu-dit":"Avize","lat":	48.977	,"lng":	4.001	,"alt":	175	},
{	"commune":"Bouzy","lieu-dit":"Bouzy","lat":	49.091	,"lng":	4.149	,"alt":	153	},
{	"commune":"Chatillon sur Marne","lieu-dit":"Chatillon","lat":	49.098	,"lng":	3.759	,"alt":	153	},
{	"commune":"Germaine","lieu-dit":"Germaine","lat":	49.123	,"lng":	4.032	,"alt":	172	},
{	"commune":"Chambrecy","lieu-dit":"Chambrecy","lat":	49.174	,"lng":	3.836	,"alt":	123	},
{	"commune":"Mailly-Champagne","lieu-dit":"Mailly","lat":	49.155	,"lng":	4.116	,"alt":	182	},
{	"commune":"Vert-Toulon","lieu-dit":"Vertoul","lat":	48.84	,"lng":	3.905	,"alt":	155	},
{	"commune":"Vertus","lieu-dit":"Vertus","lat":	48.902	,"lng":	3.995	,"alt":	150	},
{	"commune":"Saint-Thierry","lieu-dit":"Sthierry","lat":	49.3	,"lng":	3.96	,"alt":	135	},
{	"commune":"Les Riceys","lieu-dit":"Riceys","lat":	47.981	,"lng":	4.33	,"alt":	274	},
{	"commune":"Essoyes","lieu-dit":"Essoyes","lat":	48.039	,"lng":	4.493	,"alt":	280	},
{	"commune":"Colombé-la-Fosse","lieu-dit":"Colombe","lat":	48.261	,"lng":	4.779	,"alt":	252	},
{	"commune":"Vitry-le-Croisé","lieu-dit":"Vitry","lat":	48.144	,"lng":	4.554	,"alt":	237	},
{	"commune":"Prunay","lieu-dit":"Aérodrome de Reims Prunay","lat":	49.21	,"lng":	4.16	,"alt":	95	},
{	"commune":"Braine","lieu-dit":"Ferme du parc","lat":	49.35	,"lng":	3.53	,"alt":	61	},
{	"commune":"Changis","lieu-dit":"Pont de l'ormois","lat":	48.97	,"lng":	3.01	,"alt":	70	},
{	"commune":"Esternay","lieu-dit":"Exploitation Dandre","lat":	48.74	,"lng":	3.58	,"alt":	184	},
{	"commune":"Bouy-sur-Orvin","lieu-dit":"Le-Clos-De-Macon","lat":	48.44	,"lng":	3.51	,"alt":	101	},
{	"commune":"St Mard-en-Othe","lieu-dit":"RD15","lat":	48.17	,"lng":	3.79	,"alt":	226	},
{	"commune":"Celles-sur-Ource","lieu-dit":"Bourg","lat":	48.07	,"lng":	4.41	,"alt":	275	},
{	"commune":"Chaumont-Semoutier","lieu-dit":"Aérodrome","lat":	48.09	,"lng":	5.05	,"alt":	300	},
{	"commune":"Mathaux-Etape","lieu-dit":"L'Etape","lat":	48.35	,"lng":	4.47	,"alt":	143	},
{	"commune":"St-Dizier","lieu-dit":"Robinson","lat":	48.63	,"lng":	4.9	,"alt":	139	},
{	"commune":"Vatry","lieu-dit":"Aéroport","lat":	48.78	,"lng":	4.17	,"alt":	179	},
{	"commune":"Mourmelon-le- Grand","lieu-dit":"Bourg","lat":	49.11	,"lng":	4.36	,"alt":	115	},
{	"commune":"Troyes-Barberey","lieu-dit":"Aérodrome","lat":	48.3255	,"lng":	4.0117	,"alt":	119	}
]
result=[]
for station in stationsComiteChampagne :
    print station["commune"],station["lieu-dit"],station["lat"],station["lng"],station["alt"]
    res={}
    res["station"]=station
    res["previsions"]=[]
    previs= previsions ("0025","Tmin(h)",station["lng"],station["lat"],niveau=2.0)
    for previ in previs["previsions"]:
        res["previsions"].append(
            {"date":previ["date"],"Tmini 2m":previ["valeur"]})
        print ("date:"+str(previ["date"])+"  Tmini 2m:"+str(previ["valeur"]))
    result.append(res)
#print (json.dumps(result, indent=4))
    