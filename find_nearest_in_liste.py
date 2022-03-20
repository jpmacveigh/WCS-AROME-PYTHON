import numpy as np
def find_nearest_in_liste (liste,valeur):
  """
  Retourne l'index et la valeur de l'élément de la "liste" le plus proche de "valeur"
  """
  array=np.asarray(liste)
  idx=(np.abs(array-valeur)).argmin()
  return ((idx,array[idx])) 