import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d 
import matplotlib.pyplot as plt

lista_previa = [[0, 0, 0, 1, 1, 1, 2,  2, 2], [0, 1, 2, 0, 1, 2, 0, 1 ,2]]

lista_futura = list()
for i in range (0, len(lista_previa[0])): 
   #lista_futura.append([float(lista_previa[0][i]), float(lista_previa[1][i])])
   lista_futura.append([lista_previa[0][i], lista_previa[1][i]])

points = np.array(lista_futura)
print(points)
#points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])
vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.show()