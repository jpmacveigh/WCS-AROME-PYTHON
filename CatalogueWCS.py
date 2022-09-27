# -*- coding: utf-8 -*-
# coding: utf8
import json
class CatalogueWCS:
    catalogueWCS={
    "Tourab(p)":("ABSOLUTE_VORTICITY__ISOBARIC_SURFACE","Tourbillon absolu sur des surfaces isobares","dynamique",4),
    "Br10.8":("BRIGHTNESS_TEMPERATURE__GROUND_OR_WATER_SURFACE","Température de brillance dans le canal infrarouge 10.8 microns","rayonnement",3),
    "Cape":("CONVECTIVE_AVAILABLE_POTENTIAL_ENERGY__GROUND_OR_WATER_SURFACE","CAPE de la particule la plus instable en basses couches avec coefficient d'entraînement","convection",3),
    "NebConv":("CONVECTIVE_CLOUD_COVER__GROUND_OR_WATER_SURFACE","Nébulosité associée à la convection","nébulosité",3),
    "Dp(p)":("DEW_POINT_TEMPERATURE__ISOBARIC_SURFACE","Température du point de rosée sur des surfaces isobares","point de rosée",4),
    "Dp(h)":("DEW_POINT_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Température du point de rosée en niveaux hauteur","point de rosée",4),
    "Fluxvis (cumul)":("DOWNWARD_SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE","Flux solaire descendant","rayonnement",3),
    "Topo":("GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE","Altitude géométrique","topographie",3),
    "Geop(p)":("GEOPOTENTIAL__ISOBARIC_SURFACE","Altitude géopotentielle sur des surfaces isobares","géopotentiel",4),
    "NebHigh":("HIGH_CLOUD_COVER__GROUND_OR_WATER_SURFACE","Nébulosité de l'étage supérieur","nébulosité",3),
    "Nlow":("LOW_CLOUD_COVER__GROUND_OR_WATER_SURFACE","Nébulosité de l'étage inférieur","nébulosité",3),
    "Tmax(h)":("MAXIMUM_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Température maximale de l'air en niveaux hauteur","température",4),
    "NebMed":("MEDIUM_CLOUD_COVER__GROUND_OR_WATER_SURFACE","Nébulosité de l'étage moyen","nébulosité",3),
    "Tmin(h)":("MINIMUM_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Température minimale de l'air en niveaux hauteur","température",4),
    "Hcli":("PLANETARY_BOUNDARY_LAYER_HEIGHT__GROUND_OR_WATER_SURFACE","Hauteur de la couche limite","turbulence",3),
    "Tourpot(p)":("POTENTIAL_VORTICITY__ISOBARIC_SURFACE","Tourbillon potentiel sur des surfaces isobares","dynamique",4),
    "Psol":("PRESSURE__GROUND_OR_WATER_SURFACE","Pression sol","pression",3),
    "Pmer":("PRESSURE__MEAN_SEA_LEVEL","Pression réduite au niveau de la mer","pression",3),
    "P(h)":("PRESSURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Pression en niveaux hauteur","pression",4),
    "Teta(p)":("PSEUDO_ADIABATIC_POTENTIAL_TEMPERATURE__ISOBARIC_SURFACE","Température pseudo-adiabatique potentielle du thermomètre mouillé sur des surfaces isobares","température",4),
    "Hum(p)":("RELATIVE_HUMIDITY__ISOBARIC_SURFACE","Humidité relative sur des surfaces isobares","humidité",4),
    "Hum(h)":("RELATIVE_HUMIDITY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Humidité relative en niveaux hauteur","humidité",4),
    "Fluxshort (cumul)":("SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE","Flux solaire","rayonnement",3),
    "Cloudice(p)":("SPECIFIC_CLOUD_ICE_WATER_CONTENT__ISOBARIC_SURFACE","Glace nuageuse sur des surfaces isobares","précipitations",4),
    "Cloudice(h)":("SPECIFIC_CLOUD_ICE_WATER_CONTENT__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Glace nuageuse en niveaux hauteur","précipitations",4),
    "Rain(p)":("SPECIFIC_RAIN_WATER_CONTENT__ISOBARIC_SURFACE","Contenu en eau sous forme de pluie du nuage sur des surfaces isobares","précipitations",4),
    "Rain(h)":("SPECIFIC_RAIN_WATER_CONTENT__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Contenu en eau sous forme de pluie du nuage en niveaux hauteur","précipitations",4),
    "Snow(p)":("SPECIFIC_SNOW_WATER_CONTENT__ISOBARIC_SURFACE","Contenu en eau sous forme de neige du nuage sur des surfaces isobares","précipitations",4),
    "Snow(h)":("SPECIFIC_SNOW_WATER_CONTENT__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Contenu en eau sous forme de neige du nuage en niveaux hauteur","précipitations",4),
    "Tsol":("TEMPERATURE__GROUND_OR_WATER_SURFACE","Température de surface","température",3),
    "T(p)":("TEMPERATURE__ISOBARIC_SURFACE","Température de l'air sur des surfaces isobares","température",4),
    "T(h)":("TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Température de l'air en niveaux hauteur","température",4),
    "NebTot":("TOTAL_CLOUD_COVER__GROUND_OR_WATER_SURFACE","Nébulosité totale","nébulosité",3),
    "RR(p)":("TOTAL_PRECIPITATION_RATE__ISOBARIC_SURFACE","Intensité des précipitations sur des surfaces isobares","précipitations",4),
    "RR(h)":("TOTAL_PRECIPITATION_RATE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Intensité des précipitations en niveaux hauteur","précipitations",4),
    "Precip (cumul)":("TOTAL_PRECIPITATION__GROUND_OR_WATER_SURFACE","Quantité totale de précipitations","précipitations",3),
    "Precip? (cumul)":("TOTAL_PRECIPITATION_RATE__GROUND_OR_WATER_SURFACE","Quantité totale de précipitations ?","précipitations",3),
    "Snow (cumul)":("TOTAL_SNOW_PRECIPITATION__GROUND_OR_WATER_SURFACE","Quantité de précipitations sous forme de neige","précipitations",3),
    "RR(cumul)":("TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE","Quantité de précipitations sous forme liquide","précipitations",3),
    "Kte(p)":("TURBULENT_KINETIC_ENERGY__ISOBARIC_SURFACE","Energie cinétique turbulente sur des surfaces isobares","turbulence",4),
    "Kte(h)":("TURBULENT_KINETIC_ENERGY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Energie cinétique turbulente en niveaux hauteur","turbulence",4),
    "Ugust(h)":("U_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","composante zonale de la rafale du vent, en niveaux hauteur","vent",4),
    "U(p)":("U_COMPONENT_OF_WIND__ISOBARIC_SURFACE","composante zonale du vent, sur des surfaces isobares","vent",4),
    "U1.5":("U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_1500","composante zonale du vent, sur la surface 1.5 PVU","vent",3),
    "U2.0":("U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_2000","composante zonale du vent, sur la surface 2.0 PVU","vent",3),
    "U(h)":("U_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","composante zonale du vent, en niveaux hauteur","vent",4),
    "Vzm(p)":("VERTICAL_VELOCITY_GEOMETRIC__ISOBARIC_SURFACE","Vitesse verticale sur des surfaces isobares","vitesse verticale",4),
    "VzPa(p)":("VERTICAL_VELOCITY_PRESSURE__ISOBARIC_SURFACE","Vitesse verticale sur des surfaces isobares","vitesse verticale",4),
    "Vgust(h)":("V_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","composante méridienne de la rafale du vent, en niveau hauteur","vent",4),
    "V(p)":("V_COMPONENT_OF_WIND__ISOBARIC_SURFACE","composante méridienne du vent, sur des surfaces isobares","vent",4),
    "V1.5":("V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_1500","composante méridienne du vent, sur la surface 1.5 PVU","vent",3),
    "V2.0":("V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_2000","composante méridienne du vent, sur la surface 2.0 PVU","vent",3),
    "V(h)":("V_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","composante méridienne du vent, en niveau hauteur","vent",4),
    "FFgust(h)":("WIND_SPEED_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Rafale de vent en niveaux hauteur","vent",4),
    "FF(p)":("WIND_SPEED__ISOBARIC_SURFACE","Force du vent sur des surfaces isobares","vent",4),
    "FF(h)":("WIND_SPEED__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND","Force du vent en niveaux hauteur","vent",4)}

#print([CatalogueWCS.catalogueWCS[x] for x in CatalogueWCS.catalogueWCS])
"""
tri=sorted([CatalogueWCS.catalogueWCS[x] for x in CatalogueWCS.catalogueWCS],key=lambda x:x[2])
for i in tri:
    print(i)
print (len(tri))


cles=[]
for (k,v) in CatalogueWCS.catalogueWCS.items():
    cles.append((k,v))
cles.sort()

for cle in cles :
    (k,v)=cle
    (Id,desc,classe)=v
    print (k + "   "+desc+"   "+classe)
print (len(cles))
#print (json.dumps(cles))

"""